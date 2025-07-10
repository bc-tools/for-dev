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

def get_relpaths(onedir):
# WARNING! "No status" implies "No parser to add".
    status_dir = onedir / "STATUS"
    files      = []

    for yaml_file in status_dir.glob("**/*.yaml"):
        status_data = safe_load(yaml_file.read_text())

        if status_data[TAG_STATUS] != TAG_OK:
            continue

        reldir       = yaml_file.relative_to(status_dir)
        relpath      = reldir.parent / f"{reldir.stem}.py"
        contrib_file = onedir / relpath

        if not contrib_file.is_file():
            raise IOError(f"missing file:\n{contrib_file}")

        files.append((relpath, contrib_file))

    return files


# ------------ #
# -- PARSER -- #
# ------------ #

parser_contrib_dir = CONTRIB_DIR / "parser"
parser_src_dir = SRC_DIR / "parser"

for relpath, contrib_file in get_relpaths(parser_contrib_dir):
    print(f"+ ''{relpath}'' new parser.")

    src_file = parser_src_dir / relpath

    src_file.parent.mkdir(
        parents  = True,
        exist_ok = True
    )

    src_file.touch()
    src_file.write_text(
        contrib_file.read_text()
    )
