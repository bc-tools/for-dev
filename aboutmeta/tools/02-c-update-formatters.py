#!/usr/bin/env python3

from typing import List, Set, Dict

from pathlib import Path
import              re
from yaml    import safe_load

from black import (
    format_file_in_place,
    FileMode,
    WriteBack
)


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent

PROJECT_DIR  = THIS_DIR.parent
PROJECT_NAME = PROJECT_DIR.name

SPECS_DIR = PROJECT_DIR / "specs"

SRC_DIR      = PROJECT_DIR / "src" / PROJECT_NAME
FORMATTERS_FILE = SRC_DIR / "data" / "formatters.py"

FORMATTERS = []

TAG_EMPTY_LINE = "EMPTY_LINE"


# ----------- #
# -- TOOLS -- #
# ----------- #

def extract_formatters(yaml_file):
    global FORMATTERS

    src_code = yaml_file.read_text()

    last_level = 100 # Bigger than any real level!
    cur_paths  = []

    directives = []

    for line in src_code.split("\n"):
        if not line:
            directives.append(TAG_EMPTY_LINE)

        elif line[0] == "#":
            continue

        else:
            level = (len(line) - len(line.lstrip())) // 2

            if level <= last_level:
                for _ in range(last_level - level + 1):
                    if not cur_paths:
                        break

                    cur_paths.pop(-1)

            last_level = level

            keys = line.split(':')[0]
            keys = keys.strip()

            if keys[-1] == "*":
                keys = keys[:-1]
                keys = keys.strip()

            for k in keys.split('|'):
                directives.append(
                    '.'.join(cur_paths + [k.strip()])
                )

            cur_paths.append(k)

    directives = directives[:-1]

    return directives


# ------------------------------------- #
# -- ANALYZING SOURCES OF YAML SPECS -- #
# ------------------------------------- #

for yaml_file in sorted(SPECS_DIR.glob("*.yaml")):
    directives = extract_formatters(yaml_file)

    if FORMATTERS:
        FORMATTERS += [TAG_EMPTY_LINE]*2

    FORMATTERS += directives

pyspecs = f"{FORMATTERS}"
pyspecs = pyspecs.replace(
    f'{TAG_EMPTY_LINE!r}',
    'TAG_EMPTY_LINE'
)

# Nothing left to do.
FORMATTERS_FILE.touch()
FORMATTERS_FILE.write_text(
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

TAG_EMPTY_LINE = {TAG_EMPTY_LINE!r}


# --------------------------- #
# -- FORMATTING DIRECTIVES -- #
# --------------------------- #

FORMATTERS = {pyspecs}
    """.strip() + '\n'
)

format_file_in_place(
    FORMATTERS_FILE,
    fast       = False,
    mode       = FileMode(),
    write_back = WriteBack.YES,
)
