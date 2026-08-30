#!/usr/bin/env python3

# IMPORTANT.
#
# The data analyzed was previously validated by a script used
# to build the final spec validators. Therefore, we can trust
# the structure of the YAML files analyzed.

from typing import Any

from pathlib import Path
import              sys

TOOLS_DIR = Path(__file__).parent

while TOOLS_DIR.name != "tools":
    TOOLS_DIR = TOOLS_DIR.parent

sys.path.append(str(TOOLS_DIR))

from cbutils               import *
from projutils.constants   import *
from projutils.fake_tnsdoc import *
from projutils.keymgr      import *


from collections.abc import Iterator

from shutil import rmtree


# --------------- #
# -- CONSTANTS -- #
# --------------- #

SRC_DIR        = TOOLS_DIR.parent
CONTRIBUTE_DIR = SRC_DIR / "contribute"
EN_API_DIR     = CONTRIBUTE_DIR / "translate" / "en" / "api"

BLOCK_FLAVOUR_SPEC_DIR = CONTRIBUTE_DIR / "api" / "block-n-flavour"

CONTRIB_DIRS = [
    p
    for p in BLOCK_FLAVOUR_SPEC_DIR.glob('*')
    if (
        p.name not in [
            'changes',
            'readme',
        ]
        and
        p.name[0] != '.'
    )
]


# ----------- #
# -- TOOLS -- #
# ----------- #

def yaml_comment_2_tnsdoc(line_iter : Iterator[str]) -> str:
    lines = [MAGIC_COMMENT_DELIM]

    for l in line_iter:
        l = l.strip()

        if(not l or l[0] != '#'):
            raise ValueError('Illegal magic comment!')

        lines.append(l)

        if l == MAGIC_COMMENT_DELIM:
            break

    if(
        len(lines) == 1
        or
        lines[-1] != MAGIC_COMMENT_DELIM
    ):
        raise ValueError('Illegal magic comment!')

    tnsdoc = comment_2_tnsdoc('\n'.join(lines))

    return tnsdoc

def extract_tnsdoc(
    blockname: str,
    content  : str
) -> dict[str, Any]:
    alldocs = {
        TAG_MAIN_DOC: '',
    }

    lines_iter = iter(content.strip().splitlines())

# Main mandatory doc extraction.
    l = next(lines_iter)

    if l != MAGIC_COMMENT_DELIM:
        raise ValueError(
            'Missing mandatory main doc via magic comment'
        )

    magic_comment = yaml_comment_2_tnsdoc(lines_iter)

    if magic_comment == '':
        raise ValueError(
            'Missing mandatory main doc via magic comment'
        )

    alldocs[TAG_MAIN_DOC] = magic_comment

# Optional key docs extraction.
    magic_comment = ''
    last_keys     = []

    for l in lines_iter:
# One new magic comment.
        if l.rstrip() == MAGIC_COMMENT_DELIM:
            magic_comment = yaml_comment_2_tnsdoc(lines_iter)

# YAML key/val.
        elif(
            l.strip()
            and
            l.strip()[0] != '#'
        ):
            level = get_level(l)

            key, _ , val = l.partition(":")

            key = get_mainkey(key)
            val =val.strip()

            while(len(last_keys) >= level):
                last_keys.pop()

            last_keys.append(key)

            if magic_comment:
                p = '.'.join(last_keys)

                alldocs[p] = magic_comment

            magic_comment = ''

# Nothing left to do.
    return alldocs


# ------------------- #
# -- DEBUG - START -- #
# content =  """
# ###
# # MAIN
# #
# #DOC
# ###
# a:
# ###
# # X
# # X
# ###
#   x:ok

#   y: ko?

# b: dac

# c:
#   d:
# ###
# # E
# ###
#     e:
#       - lll
# """

# alldocs = extract_tnsdoc(content)

# from pprint import pprint
# pprint(alldocs)

# exit()
# -- DEBUG - END -- #
# ----------------- #


# ---------------------------- #
# -- REMOVE ALL EN API DOCS -- #
# ---------------------------- #

if not EN_API_DIR.is_dir():
    EN_API_DIR.mkdir()

else:
    for p in EN_API_DIR.glob("*"):
        p.unlink() if p.is_file() else rmtree(p)


# ----------------------------- #
# -- LET'S EXTRACT METADATA! -- #
# ----------------------------- #

for onedir in CONTRIB_DIRS:
    kind = onedir.name

    logging.info(f"Working on '{kind}'.")

    kind_dir = EN_API_DIR / kind

    if not kind_dir.is_dir():
        kind_dir.mkdir()

    for folder, filenames in get_accepted_paths(onedir).items():
        for fname in filenames:
            logging.info(f"Doc of {kind}: '{fname}'.")

            contrib_path = folder / fname
            kind_name    = contrib_path.stem

            alldocs = extract_tnsdoc(
                blockname = kind_name,
                content   = contrib_path.read_text()
            )

            api_en_dir = kind_dir / kind_name

            if not api_en_dir.is_dir():
                api_en_dir.mkdir()

            for vpapth, doc in alldocs.items():
                apifile = api_en_dir / f"{vpapth}.tns.txt"

                apifile.touch()
                apifile.write_text(doc)
