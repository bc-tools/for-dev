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

CONTEXT  = 'data'
MSG_CTXT = 'data class contrib'


THIS_DIR    = Path(__file__).parent
PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'aboutmeta'):
    PROJECT_DIR = PROJECT_DIR.parent

SPECS_DIR     = PROJECT_DIR / 'src' / 'aboutmeta' / 'specs'
DATA_SPECS_DIR = SPECS_DIR / CONTEXT
CONTRIB_DIR    = PROJECT_DIR / 'contribute' / 'api' / CONTEXT


# ------------------ #
# -- CONSTANTS #2 -- #
# ------------------ #

HEADERS_MANDATORY = set([
    (SECTION_DATA := 'DATA'),
    (SECTION_TESTS:= 'TESTS'),
])

HEADERS_OPTIONAL = set([
    (SECTION_TOOLS:= 'TOOLS'),
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


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

add_missing_dir(SPECS_DIR)
empty_dir(DATA_SPECS_DIR)

for p in [
    SPECS_DIR,
    DATA_SPECS_DIR,
]:
    add_missing_init(p)


for folder, contribs in get_accepted_paths(
    context     = CONTEXT,
    contrib_dir = CONTRIB_DIR
).items():
    ctxt = folder.parent.name

    logging.info(f"Working on '{ctxt}' codes.")

    for one_contrib in contribs:
# New Python code.
        contrib_file = folder / one_contrib

# Magic coments welle used?
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

# Add the original source used.
        final_code = add_pysrc_used(
            code     = final_code,
            path_src = contrib_file.relative_to(PROJECT_DIR.parent)
        )


# We can create / update the source file.
        create_update_file(
            file    = DATA_SPECS_DIR / one_contrib,
            content = final_code,
        )

# Extra files to add?
        xtra_files = get_xtra_files(contrib_file)

        if xtra_files:
            plurial = '' if len(xtra_files) == 1 else 's'

            logging.warning(f"Extra file{plurial} used.")

            for xfile in xtra_files:
                create_update_file(
                    file      = DATA_SPECS_DIR / xfile.name,
                    content   = xfile.read_text() + '\n',
                    log_level = TAG_WARNING
                )
