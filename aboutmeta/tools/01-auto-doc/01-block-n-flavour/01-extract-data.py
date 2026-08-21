#!/usr/bin/env python3


from pathlib import Path
import              sys

TOOLS_DIR = Path(__file__).parent

while TOOLS_DIR.name != "tools":
    TOOLS_DIR = TOOLS_DIR.parent

sys.path.append(str(TOOLS_DIR))

from cbutils.core import *

from ruamel.yaml import YAML

ruamel_load = YAML().load


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR    = Path(__file__).parent
PROJECT_DIR = TOOLS_DIR.parent
SRC_DIR     = PROJECT_DIR / "src" / "aboutmeta" / "specs"
CONTRIB_DIR = PROJECT_DIR / "contrib" / "api" / "block-n-flavour"

CONFIG_DIRS = [
    p / "config"
    for p in CONTRIB_DIR.glob('*')
    if (
        p.name not in [
            'changes',
            'readme',
        ]
        and
        p.name[0] != '.'
    )
]


TAG_MAIN_DOC = "..main.."


# ----------- #
# -- TOOLS -- #
# ----------- #

def comment_2_doc(comment):
    lines = [
        l.strip().lstrip("#").strip()
        for l in comment.splitlines()
    ]

    comment = "\n".join(lines)

    return comment


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

data = dict()

for onedir in CONFIG_DIRS:
    kind = onedir.parent.name

    subdata = dict()


    logging.info(f"Working on '{kind}'.")

    for p in onedir.glob('*.yaml'):
        logging.info(f"Analysing {kind}: '{p.name}'.")

        this_data = ruamel_load(p.read_text())

        subdata[p.stem] = None

    data[kind] = subdata





from pprint import pprint;pprint(data)
