#!/usr/bin/env python3

from pathlib import Path
from yaml    import safe_load

# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR     = Path(__file__).parent
PROJECT_DIR  = THIS_DIR.parent.parent
PROJECT_NAME = PROJECT_DIR.name

CONTRIB_DIR = PROJECT_DIR / "contrib"
SRC_DIR     = PROJECT_DIR / "src" / PROJECT_NAME

TAG_STATUS = "status"
TAG_OK     = "ok"


# ----------- #
# -- TOOLS -- #
# ----------- #

def get_status(onedir):
    status_dir = onedir / "STATUS"

    for yaml_file in status_dir.glob("**/*.yaml"):
        status_data = safe_load(yaml_file.read_text())

        if status_data[TAG_STATUS] != TAG_OK:
            continue

        relpath        = yaml_file.relative_to(status_dir)
        pyfile_contrib = onedir / relpath.parent / f"{relpath.stem}.py"

        if not pyfile_contrib.is_file():
            raise IOError(f"missing file:\n{pyfile_contrib}")

        pyfile_src = SRC_DIR / onedir.name / pyfile_contrib.relative_to(onedir)

        print(pyfile_src)

        exit()

# ------------ #
# -- PARSER -- #
# ------------ #

# WARNING! "No status" implies "No parser to add".

PARSER_DIR = CONTRIB_DIR / "parser"

get_status(PARSER_DIR)
