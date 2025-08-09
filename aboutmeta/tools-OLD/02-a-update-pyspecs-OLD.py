# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent

PROJECT_DIR  = THIS_DIR.parent
PROJECT_NAME = PROJECT_DIR.name

SPECS_DIR  = PROJECT_DIR / "specs"
SPECS_FILE = PROJECT_DIR / "src" / PROJECT_NAME / "data" / "specs.py"

MAGIC_GOMMENT_SPECS = f"""
# ---------------- #
# -- YAML SPECS -- #
# ---------------- #
""".strip()




# ----------- #
# -- TOOLS -- #
# ----------- #


# --------------- #
# -- PRE SPECS -- #
# --------------- #

ALL_PARSERS_FOUND = set()

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

    constants.append(f'{onevar} = "{globals()[onevar]}"')

    pyspecs = pyspecs.replace(
        f"'{globals()[onevar]}'",
        onevar
    )

# Text version of the constants.
constants = '\n'.join(constants)

# Use of tag parsers instead of hard typed texts.
ALL_PARSERS_FOUND = list(ALL_PARSERS_FOUND)
ALL_PARSERS_FOUND.sort()

tag_parsers = {}

for parser in ALL_PARSERS_FOUND:
    tag_parsers[
        tag:= f"TAG_PARSER_{parser.upper()}"
    ] = parser

    for punctuation in ",}":
        pyspecs = pyspecs.replace(
            f"'{parser}'{punctuation}",
            f"{tag}{punctuation}"
        )



tag_parsers = [
    f'{k} = "{v}"'
    for k, v in tag_parsers.items()
]

tag_parsers = '\n'.join(tag_parsers)

# Nothing left to do.
SPECS_FILE.touch()
SPECS_FILE.write_text(
    f"""
#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #


# --------------- #
# -- CONSTANTS -- #
# --------------- #

{constants}

{tag_parsers}


# ------------------------ #
# -- READY-TO-USE SPECS -- #
# ------------------------ #

SPECS = {pyspecs}
    """.strip() + '\n'
)

format_file_in_place(
    SPECS_FILE,
    fast       = False,
    mode       = FileMode(),
    write_back = WriteBack.YES,
)
