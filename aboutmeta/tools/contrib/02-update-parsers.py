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

def get_relfiles(onedir):
    status_dir = onedir / "STATUS"
    files      = []

    for yaml_file in status_dir.glob("**/*.yaml"):
        status_data = safe_load(yaml_file.read_text())

        if status_data[TAG_STATUS] != TAG_OK:
            continue

        reldir   = yaml_file.relative_to(status_dir)
        relfile  = reldir.parent / f"{reldir.stem}.py"
        fullfile = onedir / relfile

        if not fullfile.is_file():
            raise IOError(f"missing file:\n{fullfile}")


        files.append((relfile, fullfile))

    return files


# ------------ #
# -- PARSER -- #
# ------------ #

# WARNING! "No status" implies "No parser to add".

PARSER_DIR = CONTRIB_DIR / "parser"

for relfile, fullfile in get_relfiles(PARSER_DIR):
    print(f"+ ''{relfile}'' new parser.")
