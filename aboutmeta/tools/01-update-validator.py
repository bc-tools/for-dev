
#!/usr/bin/env python3

from copy    import copy
from pathlib import Path
import              re
from yaml    import safe_load

import black
from black import FileMode, WriteBack


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR     = Path(__file__).parent
PROJECT_DIR  = THIS_DIR.parent
PROJECT_NAME = PROJECT_DIR.name

SPECS_DIR  = PROJECT_DIR / "specs"
SPECS_FILE = PROJECT_DIR / "src" / "aboutmeta" / "specs.py"


MAGIC_GOMMENT_SPECS = f"""
# ---------------- #
# -- YAML SPECS -- #
# ---------------- #
""".strip()


PATTERN_SPECIAL_TAGS_SPECS = re.compile(r"__[a-z]+__")

TAG_FILE = '__file__'

SPECIAL_TAGS_SPECS = [
    TAG_ABBREV:= '__abrev__',
]


PATTERN_LIST_OF    = re.compile(r"list\((?P<kind>.*)\)")
PATTERN_LEGAL_LIST = re.compile(r"[a-zA-Z_]+(\.[a-zA-Z_]+)*")

TAG_AM_DATA        = "aboutmeta.data"
PATTERN_AM_DATA    = re.compile(fr"'{TAG_AM_DATA}\.(?P<module>[a-z]+)\.(?P<class>[a-zA-Z]+)'")

PY_TAGS = [
    TAG_ALT_ALL   := "__alternative_all__",
    TAG_ALT_TUPLES:= "__alternative_tuples__",
    TAG_BLOCK     := "__block__",
    TAG_DATA      := "__data__",
    TAG_LIST_OF   := "__list_of__",
    TAG_PARSER    := "__parser__",
    TAG_REQUIRED  := "__required__",
    TAG_TYPE      := "__type__",
]

PY_TYPES = [
    TAG_PERSON := "person",
    TAG_VERSION:= "__alternative_tuples__",
    TAG_BLOCK     := "__block__",
    TAG_DATA      := "__data__",
    TAG_LIST_OF   := "__list_of__",
    TAG_PARSER    := "__parser__",
    TAG_REQUIRED  := "__required__",
    TAG_TYPE      := "__type__",
]


TAB_1 = ' '*2
TAB_2 = TAB_1*2
TAB_3 = TAB_1*3

ITEM_1 = '+'
ITEM_2 = f'{TAB_1}*'
ITEM_3 = f'{TAB_2}-'
ITEM_4 = f'{TAB_3}-->'


# ----------- #
# -- TOOLS -- #
# ----------- #

def digested_specs(yaml_file):
    yaml_file_name = yaml_file.name

    specs = safe_load(yaml_file.read_text())

# Legal special tags?
    extradata = dict()

    for k in specs:
        if PATTERN_SPECIAL_TAGS_SPECS.fullmatch(k):
            if not k in SPECIAL_TAGS_SPECS:
                raise ValueError(
                    f"illegal special key ''{k}'' in "
                    f"''specs/{yaml_file_name}'' file."
                )

            extradata[k] = specs[k]

    for k in extradata:
        del specs[k]

    extradata[TAG_FILE] = yaml_file_name

# Let's work recursively.
    return build_pyspecs(specs, extradata)


def build_pyspecs(specs, extradata):
    pyspecs = {
        TAG_ALT_ALL: [],
        TAG_ALT_TUPLES : [],
    }

    for key, val in specs.items():
        if isinstance(val, str):
            splitted_keys = [k.strip() for k in key.split('|')]
            splitted_vals = [v.strip() for v in val.split('|')]

            if len(splitted_keys) != len(splitted_vals):
                raise ValueError(
                     "keys and types with differnet numbers of pipe in "
                    f"''specs/{extradata[TAG_FILE]}'' file."
                    f"\n  + ''{key}''"
                    f"\n  + ''{val}''"
                )

            elif len(splitted_keys) > 1:
                if key[-1] == "*":
                    splitted_keys = [
                        k[:-1].strip()
                        if k[-1] == "*" else
                        k
                        for k in  splitted_keys
                    ]

                    pyspecs[TAG_ALT_ALL] += splitted_keys

                    pyspecs[TAG_ALT_TUPLES].append(tuple(splitted_keys))

                    splitted_keys = [f"{k}*" for k in  splitted_keys]

            for k, v in zip(splitted_keys, splitted_vals):
                k, thispsec = build_single_pyspec(k, v, extradata)
                pyspecs[k]  = thispsec

        else:
            key, thispsec = build_single_pyspec(key, val, extradata)
            pyspecs[key]  = thispsec

    if pyspecs[TAG_ALT_ALL]:
        pyspecs[TAG_ALT_ALL]    = tuple(pyspecs[TAG_ALT_ALL])
        pyspecs[TAG_ALT_TUPLES] = tuple(pyspecs[TAG_ALT_TUPLES])

    else:
        pyspecs[TAG_ALT_ALL] = tuple()

        del pyspecs[TAG_ALT_TUPLES]

# Nothing left to do.
    return pyspecs


def build_single_pyspec(key, val, extradata):
    this_specs = dict()

# Key analysis.
    if key[-1] == "*":
        isrequired = False
        key        = key[:-1].strip()

    else:
        isrequired = True

    this_specs = {
        TAG_REQUIRED: isrequired
    }

# Value analysis.
    if isinstance(val, str):
        is_list_of, parser = which_parser(val, extradata)

        this_specs |= {
            TAG_TYPE   : TAG_DATA,
            TAG_LIST_OF: is_list_of,
            TAG_PARSER : parser,
        }


    else:
        this_specs[TAG_TYPE] = TAG_BLOCK

        for k, v in build_pyspecs(val, extradata).items():
            this_specs[k] = v

    return key, this_specs


def which_parser(val, extradata):
    if TAG_ABBREV in extradata:
        for oneabbrev, replacement in extradata[TAG_ABBREV].items():
            val = val.replace(f"\\{oneabbrev}", replacement)

    match = PATTERN_LIST_OF.fullmatch(val)

    if not match:
        is_list_of = False

    else:
        is_list_of = True
        val        = match.group('kind')

        if not PATTERN_LEGAL_LIST.fullmatch(val):
            raise ValueError(
                f"illegal type ''list({val})'' in "
                f"''specs/{extradata[TAG_FILE]}'' file."
            )

    if val == 'str':
        return is_list_of, None

    return is_list_of, val


# --------------- #
# -- PRE SPECS -- #
# --------------- #

print(f"{ITEM_1} Creation/update of the Python specs file.")

pyspecs = {}

for yaml_file in SPECS_DIR.glob("*.yaml"):
    pyspecs[yaml_file.stem] = digested_specs(yaml_file)


# ------------------------------ #
# -- BUILD FINAL PYTHON SPECS -- #
# ------------------------------ #

# Use of tags instead of hard typed texts.
pyspecs = f"{pyspecs}"

allvars = copy(globals())

constants = []

for onevar in allvars:
    if not globals()[onevar] in PY_TAGS:
        continue

    pyspecs = pyspecs.replace(
        f"'{globals()[onevar]}'",
        onevar
    )

    constants.append(f'{onevar} = "{globals()[onevar]}"')

constants = '\n'.join(constants)

# # ''aboutemeta.data'' objects instead of hard typed texts.
# imports_needed = set(PATTERN_AM_DATA.findall(pyspecs))

# for module_name, cls_name in imports_needed:
#     pyspecs = pyspecs.replace(
#         f"'{TAG_AM_DATA}.{module_name}.{cls_name}'",
#         f"{module_name}.{cls_name}"
#     )

# imports_needed = [f"    {m}," for m, c in imports_needed]
# imports_needed.sort()
# imports_needed = '\n'.join(imports_needed)

# Nothing left to do.
SPECS_FILE.write_text(
    f"""
#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project “black.”    -- #
# ------------------------------------------------------- #


# --------------- #
# -- CONSTANTS -- #
# --------------- #

{constants}


# ------------------------ #
# -- READY-TO-USE SPECS -- #
# ------------------------ #

YAML_SPECS = {pyspecs}
    """.strip() + '\n'
)

black.format_file_in_place(
    SPECS_FILE,
    fast       = False,
    mode       = FileMode(),
    write_back = WriteBack.YES,
)
