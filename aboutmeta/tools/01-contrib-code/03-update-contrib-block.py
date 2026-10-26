#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.logconf    import *
from cbutils.pathplus   import *
from cbutils.coding_py  import *
from cbutils.contrib    import *

from projutils.yaml2py import *


# ------------------ #
# -- CONSTANTS #1 -- #
# ------------------ #

CONTEXT  = 'block'
MSG_CTXT = f'{CONTEXT} config contrib'


THIS_DIR    = Path(__file__).parent
PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'aboutmeta'):
    PROJECT_DIR = PROJECT_DIR.parent

SPECS_DIR       = PROJECT_DIR / 'src' / 'aboutmeta' / 'specs'
BLOCK_PARSERS_DIR = SPECS_DIR / CONTEXT
CONTRIB_DIR     = (
      PROJECT_DIR / 'contribute' / 'api'
    / 'block-n-flavour' / CONTEXT
)

THIS_FILE_RELATIVE = (
      Path('aboutmeta')
    / Path(__file__).relative_to(PROJECT_DIR)
)

CONTRIB_CFG_DIR_RELATIVE = (
      Path('aboutmeta')
    / CONTRIB_DIR.relative_to(PROJECT_DIR)
    / 'config'
)


# ------------ #
# -- TYPING -- #
# ------------ #

type NestedStrDictType = dict[
    str,
    NestedStrDictType | str
]


# ----------- #
# -- TOOLS -- #
# ----------- #

def prestr_2_pyvar(name):
    return f'@{name}@'


def build_parsers_needed(
    parsers_needed: set[ParserSpecs],
    yaml_specs    : NestedParserDictType,
) -> None:
    for k, v in yaml_specs.items():
        if isinstance(v, ParserSpecs):
            if v.module != TAG_STR:
                parsers_needed.add(v.module)

        else:
            build_parsers_needed(
                parsers_needed = parsers_needed,
                yaml_specs     = v,
            )


def get_pyspecs(
    shortcuts_used: dict[str, ParserSpecs],
    yaml_specs    : NestedParserDictType
) -> NestedStrDictType:
    pyspecs = dict()

    for k, v in yaml_specs.items():
        if isinstance(v, ParserSpecs):
            shortcut = (
                f'__PARSER_{v.module.upper()}'
                f'_{v.datatype.upper()}'
            )

            if v.use_post:
                shortcut += '_USE_POST'

            shortcut = prestr_2_pyvar(shortcut)

            if not shortcut in shortcuts_used:
                shortcuts_used[shortcut] = {
                    prestr_2_pyvar(k): prestr_2_pyvar(v)
                    for k, v in {
                        'TAG_PARSER'  : v.module,
                        'TAG_USE_POST': v.use_post,
                        'TAG_DATATYPE': f'TAG_{v.datatype.upper()}',
                    }.items()
                }

            pyspecs[k] = shortcut

        else:
            pyspecs[k] = get_pyspecs(
                shortcuts_used = shortcuts_used,
                yaml_specs     = v
            )

    return pyspecs


SET_MANDATORY_PARSED = set([
    TAG_IS_MANDATORY,
    TAG_IS_PARSED
])


def get_pystatus(
    shortcuts_used: dict[str, ParserSpecs],
    status        : NestedBoolDictType
) -> NestedStrDictType:
    pystatus = dict()

    for k, v in status.items():
        if not isinstance(v, dict):
            pystatus[k] = v

            continue

        if set(v) == SET_MANDATORY_PARSED:
            shortcut  = '__STATUS_'
            shortcut += (
                'MANDATORY'
                if v[TAG_IS_MANDATORY] else
                'OPTIONAL'
            )

            shortcut += '_'

            if not v[TAG_IS_PARSED]:
                shortcut += 'UN'

            shortcut += 'PARSED'
            shortcut  = prestr_2_pyvar(shortcut)

            if not shortcut in shortcuts_used:
                shortcuts_used[shortcut] = {
                    prestr_2_pyvar(k): v
                    for k, v in {
                        'TAG_IS_MANDATORY': v[TAG_IS_MANDATORY],
                        'TAG_IS_PARSED'   : v[TAG_IS_PARSED],
                    }.items()
                }

            pystatus[k] = shortcut

        else:
            pystatus[k] = get_pystatus(
                shortcuts_used = shortcuts_used,
                status         = v
            )

    return pystatus


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

for f in [
    empty_dir,
    add_missing_init,
]:
    f(BLOCK_PARSERS_DIR)


for folder, contribs in get_accepted_paths(
    context     = CONTEXT,
    contrib_dir = CONTRIB_DIR
).items():
    ctxt = folder.parent.name

    logging.info(f"Working on '{ctxt}' configs.")

    for one_contrib in contribs:
        logging.info(f"Analyzing '{one_contrib}'.")

        contrib_file = folder / one_contrib

        digested_yaml = DigestedYamlSpecs(contrib_file)
        digested_yaml.build()

# # DEBUG - START
#         from pprint import pprint
#         print('---')
#         pprint(digested_yaml.parsers)
#         print('---')
#         print(digested_yaml.status.to_json(indent=4))
#         print('---')
#         print(digested_yaml.alts)#.to_json(indent=4))
#         # exit()
# # DEBUG - END


# The parsers to import.
        parsers_needed = set()

        build_parsers_needed(
            parsers_needed = parsers_needed,
            yaml_specs     = digested_yaml.parsers,
        )

        shortcuts_used = dict()

        pyspecs = get_pyspecs(
            shortcuts_used = shortcuts_used,
            yaml_specs     = digested_yaml.parsers,
        )

        pystatus = get_pystatus(
            shortcuts_used = shortcuts_used,
            status         = digested_yaml.status,
        )

# # DEBUG - START
#         from pprint import pprint
#         print('---')
#         pprint(parsers_needed)
#         # exit()
# # DEBUG - END


# Let's build the Python code.
        imports_need = ', '.join(
            sorted(parsers_needed)
        )

        shortcuts_code = '\n\n'.join(
            f"'{k}' = {shortcuts_used[k]}"
            for k in sorted(shortcuts_used)
        )

        block_spec_pycode = f'''
{SHEBANG_PYTHON}

# File automatically generated by
# '{THIS_FILE_RELATIVE}'
#
# This block is maintained inside the file
# '{CONTRIB_CFG_DIR_RELATIVE / one_contrib}'

{magic_title('IMPORTS')}

from benedict import benedict

from aboutmeta.core.constants import *
from aboutmeta.parsers.parser   import {imports_need}


{magic_title('INTERNAL SHORTCUTS')}

{shortcuts_code}


{magic_title('BLOCK SPECS')}

BLOCK_PARSERS = benedict({pyspecs})

BLOCK_STATUS = benedict({pystatus})

BLOCK_ALTS = benedict({digested_yaml.alts})
        '''.strip() + '\n'

        for old, new in [
            ("'__", "'@TAG_"),
            ("__'", "@'"),
        ]:
            block_spec_pycode = block_spec_pycode.replace(
                old, new
            )

        for to_remove in [
            "'@",
            "@'",
        ]:
            block_spec_pycode = block_spec_pycode.replace(
                to_remove, ''
            )

        add_black_pyfile(
            code = block_spec_pycode,
            file = BLOCK_PARSERS_DIR / f'{contrib_file.stem}.py'
        )
