#!/usr/bin/env python3

from typing import Any

from pathlib import Path
import              sys

TOOLS_DIR = Path(__file__).parent

while TOOLS_DIR.name != "tools":
    TOOLS_DIR = TOOLS_DIR.parent

sys.path.append(str(TOOLS_DIR))

from cbutils.core          import *
from projutils.constants   import *
from projutils.fake_tnsdoc import *


from collections.abc import Iterator


# --------------- #
# -- CONSTANTS -- #
# --------------- #

SRC_DIR     = TOOLS_DIR.parent
CONTRIB_DIR = SRC_DIR / "contrib" / "api" / "block-n-flavour"


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


# ----------- #
# -- TOOLS -- #
# ----------- #

def get_level(line: str) -> str:
    return 1 + (len(line) - len(line.lstrip())) // 2


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


def is_bigger_path(
    prepaths = list[list[str]],
    one_path = list[str]
) -> bool:
    if not prepaths:
        return False

    last_path = prepaths[-1]

    if(
        len(one_path) <= len(last_path)
        and
        one_path != last_path
    ):
        return False

    return True


def extract_tnsdoc(content: str) -> dict[Any]:
    alldocs = {
        TAG_FULL_PATHS: [],
        TAG_MAIN_DOC  : '',
        TAG_SUB_DOCS  : dict()
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
    prepaths      = []
    last_keys     = []
    magic_comment = ''

    for l in lines_iter:
# One new magic comment.
        if l.rstrip() == MAGIC_COMMENT_DELIM:
            magic_comment = yaml_comment_2_tnsdoc(lines_iter)

# YAML key/val.
        elif(
            l.strip()
            and
            l.strip()[0] != '#'
            and
            ":" in l
        ):
            level = get_level(l)

            key, _ , _ = l.partition(":")
            key        = key.strip()

            while(len(last_keys) >= level):
                last_keys.pop()

            last_keys.append(key)

            if is_bigger_path(
                prepaths = prepaths,
                one_path = last_keys
            ):
                prepaths[-1] = last_keys[:]

            else:
                prepaths.append(last_keys[:])

            if magic_comment:
                alldocs[TAG_SUB_DOCS][
                    '.'.join(last_keys)
                ] = magic_comment

            magic_comment = ''

# Other content clears the last doc.
        else:
            magic_comment = ''

# Let's store all the full paths.
    alldocs[TAG_FULL_PATHS] = tuple(
        tuple(p)
        for p in prepaths
    )

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


# ----------------------------- #
# -- LET'S EXTRACT METADATA! -- #
# ----------------------------- #

for onedir in CONFIG_DIRS:
    kind = onedir.parent.name

    if kind == 'flavour':
        continue

    sub_metadata = dict()

    logging.info(f"Working on '{kind}'.")

    for p in onedir.glob('*.yaml'):
        logging.info(f"Doc of {kind}: '{p.name}'.")

        alldocs = extract_tnsdoc(content = p.read_text())

# -- DEBUG - START -- #
        del alldocs[TAG_MAIN_DOC]
        from pprint import pprint;pprint(alldocs)
# -- DEBUG - END -- #
