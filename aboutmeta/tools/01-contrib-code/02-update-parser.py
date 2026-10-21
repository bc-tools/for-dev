#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.logconf    import *
from cbutils.split_file import *
from cbutils.coding_py  import *
from cbutils.contrib    import *
from cbutils.pathplus   import *


# ------------------ #
# -- CONSTANTS #1 -- #
# ------------------ #

CONTEXT  = 'parser'
MSG_CTXT = 'parser utils contrib'


THIS_DIR    = Path(__file__).parent
PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'aboutmeta'):
    PROJECT_DIR = PROJECT_DIR.parent

SPECS_DIR        = PROJECT_DIR / 'src' / 'aboutmeta' / 'specs'
PARSER_SPECS_DIR = SPECS_DIR / CONTEXT
CONTRIB_DIR      = PROJECT_DIR / 'contribute' / 'api' / CONTEXT


# ------------------ #
# -- CONSTANTS #2 -- #
# ------------------ #

HEADERS_MANDATORY = set([
    (SECTION_PARSER:= 'PARSER'),
    (SECTION_WRITER:= 'WRITER'),
    (SECTION_TESTS := 'TESTS'),
])

HEADERS_OPTIONAL = set([
    (SECTION_MAPPERS:= 'MAPPERS'),
    (SECTION_TOOLS  := 'TOOLS'),
])

HEADERS_IGNORED = set([
    SECTION_TESTS,
    SECTION_TOOLS
])


assert HEADERS_MANDATORY & HEADERS_OPTIONAL == set(), \
       f'{HEADERS_MANDATORY & HEADERS_OPTIONAL = }'

assert HEADERS_IGNORED <= (
    HEADERS_MANDATORY | HEADERS_OPTIONAL
), (
    f'{HEADERS_IGNORED = }'
     ' vs '
    f'{HEADERS_MANDATORY | HEADERS_OPTIONAL = }'
)


# ------------------ #
# -- CONSTANTS #3 -- #
# ------------------ #

FUNCS_MANDATORY = set([
    (FUNC_NAME_PARSE:= 'parse'),
    (FUNC_NAME_WRITE:= 'write'),
])

FUNCS_OPTIONAL = set([
    # (FUNC_NAME_MAP_LIST:= 'map_list'),
])

assert FUNCS_MANDATORY & FUNCS_OPTIONAL == set(), \
       f'{FUNCS_MANDATORY & FUNCS_OPTIONAL = }'


LEGAL_SIGNS = {
    FUNC_NAME_PARSE: [
        set([
            (VAR_NAME_DATA:= 'data')
        ]),
        set([
            (VAR_NAME_AMDATA_CLS:= 'amdata'),
            VAR_NAME_DATA
        ])
    ],
    FUNC_NAME_WRITE: [
        set([
            VAR_NAME_DATA
        ]),
    ]
}

assert set(LEGAL_SIGNS) == (FUNCS_MANDATORY | FUNCS_OPTIONAL), \
       f'not {set(LEGAL_SIGNS)} == {FUNCS_MANDATORY | FUNCS_OPTIONAL}'


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

for f in [
    empty_dir,
    add_missing_init,
]:
    f(PARSER_SPECS_DIR)


for folder, contribs in get_accepted_paths(
    context     = CONTEXT,
    contrib_dir = CONTRIB_DIR
).items():
    ctxt = folder.parent.name

    logging.info(f"Working on '{ctxt}' codes.")

    for one_contrib in contribs:
# New Python code.
        contrib_file = folder / one_contrib
        path_src     = contrib_file.relative_to(PROJECT_DIR.parent)

# Magic comments well used?
        hd_split_validate(
            mandatory = HEADERS_MANDATORY,
            optional  = HEADERS_OPTIONAL,
            ignored   = HEADERS_IGNORED,
            parts     = hd_split_pyfile(contrib_file),
            context   = MSG_CTXT,
        )

# Look at the code.
        final_code = finalize_pycode(
            file        = contrib_file,
            hds_ignored = HEADERS_IGNORED
        )

        if not final_code:
            log_raise_error(
                context = MSG_CTXT,
                desc    = (
                     'Empty file validated: '
                    f"'{contrib_file}'."
                ),
                exception = ValueError,
            )

# Good signatures?
        validate_signatures(
            mandatory  = FUNCS_MANDATORY,
            optional   = FUNCS_OPTIONAL,
            signatures = LEGAL_SIGNS,
            code       = final_code,
            path_src   = path_src,
            context    = MSG_CTXT,
        )

# Add the original source used.
        final_code = add_pysrc_used(
            code     = final_code,
            path_src = path_src,
        )

# We can create / update the source file.
        create_update_file(
            file    = PARSER_SPECS_DIR / one_contrib,
            content = final_code,
        )

# Extra files to add?
        xtra_files = get_xtra_files(contrib_file)

        if xtra_files:
            plurial = '' if len(xtra_files) == 1 else 's'

            logging.warning(f"Extra file{plurial} used.")

            for xfile in xtra_files:
                create_update_file(
                    file      = PARSER_SPECS_DIR / xfile.name,
                    content   = xfile.read_text() + '\n',
                    log_level = TAG_WARNING
                )
