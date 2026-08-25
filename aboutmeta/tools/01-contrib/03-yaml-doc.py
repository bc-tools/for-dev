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
CONTRIB_DIR = SRC_DIR / "contrib" / "api" / "lines-n-flavour"


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
    return (len(line) - len(line.lstrip())) // 2


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


def extract_tnsdoc(content: str) -> dict[Any]:
    all_docs = {
        TAG_MAIN_DOC: '',
        TAG_SUB_DOCS: dict()
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

    all_docs[TAG_MAIN_DOC] = magic_comment

# Optional key docs extraction.
    last_keys     = []
    magic_comment = ''

    for l in lines_iter:
# One new magic comment.
        if l.rstrip() == MAGIC_COMMENT_DELIM:
            magic_comment = yaml_comment_2_tnsdoc(lines_iter)

# YAML key/val.
        elif ":" in l:
            level = get_level(l)

            key, _ , _ = l.partition(":")
            key        = key.strip()

            if magic_comment:
                all_docs[TAG_SUB_DOCS][(key, level)] = magic_comment

            magic_comment = ''


# Other content clears the docs.
        else:
            magic_comment = ''

# Nothing left to do.
    return all_docs


# ------------------- #
# -- DEBUG - START -- #
content =  """
###
# MAIN
#
#DOC
###
a:
###
# X
# X
###
  x:ok

b: dac

c:
  d:
###
# E
###
    e:
      - lll
"""

all_docs = extract_tnsdoc(content)

from pprint import pprint
pprint(all_docs)

exit()
# -- DEBUG - END -- #
# ----------------- #










# ----------------------------- #
# -- LET'S EXTRACT METADATA! -- #
# ----------------------------- #

METADATA = dict()

for onedir in CONFIG_DIRS:
    kind = onedir.parent.name

    if kind == 'flavour':
        continue

    SUB_METADATA = dict()

    logging.info(f"Working on '{kind}'.")

    for p in onedir.glob('*.yaml'):
        logging.info(f"Doc of {kind}: '{p.name}'.")

        all_docs = extract_tnsdoc(content = p.read_text())

        SUB_METADATA[p.stem] = all_docs

    METADATA[kind] = SUB_METADATA

# -- DEBUG - START -- #
from pprint import pprint;pprint(METADATA)
# -- DEBUG - END -- #
