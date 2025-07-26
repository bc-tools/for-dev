#!/usr/bin/env python3

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

SRC_DIR         = PROJECT_DIR / "src" / PROJECT_NAME
HELPERS_FILE    = SRC_DIR / "helpers.py"
FORMATTERS_FILE = SRC_DIR / "formatters.py"

HELP_CONTENT     = {}
FORMATTING_SPECS = {}

MAGIC_COMMENT_HELPER = "#"*3


# ----------- #
# -- TOOLS -- #
# ----------- #

def extract_helpers(yaml_file):
    global HELP_CONTENT, FORMATTING_SPECS

    src_code      = yaml_file.read_text()

    is_helper_doc = False
    helper_doc    = []

    last_level       = 100 # Too big value!
    cur_pointed_path = []

    for nb, line in enumerate(
        src_code.splitlines(),
        start = 1
    ):
        if not line:
            continue

# Helping magic comment start or end?
        if line == MAGIC_COMMENT_HELPER:
            is_helper_doc = not is_helper_doc

        elif line[0] == '#':
            if is_helper_doc:
                helper_doc.append(line)

        else:
            if is_helper_doc:
                raise ValueError(
                    f"misuse of magic comments at line {nb}. "
                    f"See the file:\n{yaml_file}"
                )

            level = len(line) - len(line.lstrip()) // 2

            if level < last_level:
                for _ in range(level):
                    if not cur_pointed_path:
                        break

                    cur_pointed_path.pop(-1)

            cur_pointed_path.append(line)

            if helper_doc:
                helper_doc       = "\n".join(helper_doc)

                print(f'-- {".".join(cur_pointed_path)}')
                print(helper_doc)
                # exit()

                helper_doc       = []


# ------------------------------------- #
# -- ANALYZING SOURCES OF YAML SPECS -- #
# ------------------------------------- #

for yaml_file in SPECS_DIR.glob("*.yaml"):
    extract_helpers(yaml_file)
