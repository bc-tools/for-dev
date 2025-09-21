#!/usr/bin/env python3

from typing import List, Set, Dict

from pathlib import Path
import              re

from yaml import safe_load

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
HELPERS_FILE = SRC_DIR / "data" / "helpers.py"

HELPERS = {}

MAGIC_COMMENT_HELPER = "#"*3


PATTERN_KEEP_BEFORE_SPACES = re.compile(r'^(\s*)(.*)')
PATTERN_MULTI_SPACES       = re.compile(r'\s{2,}')
PATTERN_SECTION_TITLE      = re.compile(r'^\{(.*)\}$')


# ----------- #
# -- TOOLS -- #
# ----------- #



def gather_content(
    title          : str,
    section_content: List[str]
) -> str:
    section_content = unwrapped_content(section_content)

    if not section_content:
        TODO

    return section_content






# ------------------------------------- #
# -- ANALYZING SOURCES OF YAML SPECS -- #
# ------------------------------------- #

for yaml_file in SPECS_DIR.glob("*.yaml"):
    extract_helpers(yaml_file)

# Nothing left to do.
HELPERS_FILE.touch()
HELPERS_FILE.write_text(
    f"""
#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #


# -------------------------- #
# -- READY-TO-USE HELPERS -- #
# -------------------------- #

HELPERS = {HELPERS}
    """.strip() + '\n'
)

format_file_in_place(
    HELPERS_FILE,
    fast       = False,
    mode       = FileMode(),
    write_back = WriteBack.YES,
)
