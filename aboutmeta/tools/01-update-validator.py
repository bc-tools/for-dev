#!/usr/bin/env python3

from pathlib import Path
import              re
from yaml    import safe_load


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR     = Path(__file__).parent
PROJECT_DIR  = THIS_DIR.parent
PROJECT_NAME = PROJECT_DIR.name

SPECS_DIR = PROJECT_DIR / "specs"
SRC_DIR     = PROJECT_DIR / "src"


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
PATTERN_LEGAL_LIST = re.compile(r"[a-zA-Z_]+(.[a-zA-Z_]+)*")

TAG_BLOCK    = "__block__"
TAG_DATA     = "__data__"
TAG_LIST_OF  = "__list_of__"
TAG_PARSER   = "__parser__"
TAG_REQUIRED = "__required__"
TAG_TYPE     = "__type__"



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
    pyspecs = dict()

    for key, val in specs.items():
# Key analysis.
        if key[-1] == "*":
            isrequired = False
            key        = key[:-1]

        else:
            isrequired = True

        pyspecs[key] = {
            TAG_REQUIRED: isrequired
        }

# Value analysis.
        if isinstance(val, str):
            is_list_of, parser = which_parser(val, extradata)

            pyspecs[key][TAG_TYPE]    = TAG_DATA
            pyspecs[key][TAG_LIST_OF] = is_list_of
            pyspecs[key][TAG_PARSER]  = parser


        else:
            pyspecs[key][TAG_TYPE] = TAG_BLOCK

            for k, v in build_pyspecs(val, extradata).items():
                pyspecs[key][k] = v

# Nothing left to do.
    return pyspecs


def which_parser(val, extradata):
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

    if TAG_ABBREV in extradata:
        for oneabbrev, replacement in extradata[TAG_ABBREV].items():
            val = val.replace(f"\\{oneabbrev}", replacement)

    return is_list_of, val



# --------------------------------------------- #
# -- XXX -- #
# --------------------------------------------- #

for yaml_file in SPECS_DIR.glob("*"):#"*.yaml"):
    blockname = yaml_file.stem
    specs     = digested_specs(yaml_file)

    from pprint import pprint;pprint(specs)


# --------------------------------------------- #
# -- XXX -- #
# --------------------------------------------- #
