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


PATTERN_SPECIAL_TAGS_SPECS = re.compile(r'__[a-z]+__')

TAG_FILE = "file"

SPECIAL_TAGS_SPECS = []


PATTERN_LIST_OF    = re.compile(r"list\((?P<kind>.*)\)")
PATTERN_LEGAL_LIST = re.compile(r"[a-zA-Z_]+(\.[a-zA-Z_]+)*")

PY_TAGS = [
    TAG_SPECS_ALT_ALL   := "ALT_ALL",
    TAG_SPECS_ALT_TUPLES:= "ALT_TUPLES",
    TAG_SPECS_BLOCK     := "BLOCK",
    TAG_SPECS_CONTENT   := "CONTENT",
    TAG_SPECS_DATA      := "DATA",
    TAG_SPECS_LIST_OF   := "LIST_OF",
    TAG_SPECS_PARSER    := "PARSER",
    TAG_SPECS_REQUIRED  := "REQUIRED",
    TAG_SPECS_TYPE      := "TYPE",
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
        TAG_SPECS_ALT_ALL   : [],
        TAG_SPECS_ALT_TUPLES: [],
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

                    pyspecs[TAG_SPECS_ALT_ALL] += splitted_keys

                    pyspecs[TAG_SPECS_ALT_TUPLES].append(tuple(splitted_keys))

                    splitted_keys = [f"{k}*" for k in  splitted_keys]

            for k, v in zip(splitted_keys, splitted_vals):
                k, thispsec = build_single_pyspec(k, v, extradata)
                pyspecs[k]  = thispsec

        else:
            key, thispsec = build_single_pyspec(key, val, extradata)
            pyspecs[key]  = thispsec

    if pyspecs[TAG_SPECS_ALT_ALL]:
        pyspecs[TAG_SPECS_ALT_ALL]    = tuple(pyspecs[TAG_SPECS_ALT_ALL])
        pyspecs[TAG_SPECS_ALT_TUPLES] = tuple(pyspecs[TAG_SPECS_ALT_TUPLES])

    else:
        pyspecs[TAG_SPECS_ALT_ALL] = tuple()

        del pyspecs[TAG_SPECS_ALT_TUPLES]

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
        TAG_SPECS_REQUIRED: isrequired
    }

# Value analysis.
    if isinstance(val, str):
        is_list_of, parser = which_parser(val, extradata)

        this_specs |= {
            TAG_SPECS_TYPE   : TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: is_list_of,
            TAG_SPECS_PARSER : parser,
        }


    else:
        this_specs[TAG_SPECS_TYPE] = TAG_SPECS_BLOCK

        this_specs[TAG_SPECS_CONTENT] = build_pyspecs(val, extradata)

    return key, this_specs


def which_parser(val, extradata):
    # if TAG_ABBREV in extradata:
    #     for oneabbrev, replacement in extradata[TAG_ABBREV].items():
    #         val = val.replace(f"\\{oneabbrev}", replacement)

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

    all_parsers.add(val)

    return is_list_of, val


# --------------- #
# -- PRE SPECS -- #
# --------------- #

all_parsers = set()

print(f"{ITEM_1} Creation/update of the Python specs file.")

pyspecs = {}

for yaml_file in SPECS_DIR.glob("*.yaml"):
    pyspecs |= digested_specs(yaml_file)

# To simplify future processing, we deliberately retain
# the ''TAG_SPECS_ALT_ALL'' key.
# del pyspecs[TAG_SPECS_ALT_ALL]


# ------------------------------ #
# -- BUILD FINAL PYTHON SPECS -- #
# ------------------------------ #

# Use of tag keys instead of hard typed texts.
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

# Use of tag parsers instead of hard typed texts.
all_parsers = list(all_parsers)
all_parsers.sort()

tag_parsers = {}

for parser in all_parsers:
    tag_parsers[
        tag:= f"TAG_SPECS_PARSER_{parser.upper()}"
    ] = parser

    pyspecs = pyspecs.replace(f"'{parser}'", tag)

tag_parsers = [
    f'{k} = "{v}"'
    for k, v in tag_parsers.items()
]

tag_parsers = '\n'.join(tag_parsers)

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

{tag_parsers}


# ------------------------ #
# -- READY-TO-USE SPECS -- #
# ------------------------ #

SPECS_PARSING = {pyspecs}
    """.strip() + '\n'
)

black.format_file_in_place(
    SPECS_FILE,
    fast       = False,
    mode       = FileMode(),
    write_back = WriteBack.YES,
)
