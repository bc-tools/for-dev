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
) -> dict[Any]:
    alldocs = {
        TAG_DOC       : '',
        TAG_YAML_SPECS: '',
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

    alldocs[TAG_DOC] = magic_comment

# Optional key docs extraction.
    magic_comment = ''
    yaml_specs    = [f"{blockname}:"]
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
            if not ":" in l:
                yaml_specs.append('  ' + l.rstrip())

            else:
                level = get_level(l)

                key, _ , val = l.partition(":")
                key, val     = key.strip(), val.strip()

                indent = ' '*level*2

                if level == 1 and len(yaml_specs) != 1:
                    yaml_specs.append('')

                yaml_specs.append(f"{indent}{key}:")

                if val:
                    yaml_specs.append(f"{indent}  {val}")

                while(len(last_keys) >= level):
                    last_keys.pop()

                last_keys.append(key)

                if magic_comment:
                    data = alldocs

                    for k in last_keys:
                        if not k in data:
                            data[k] = dict()

                        data = data[k]

                    data[TAG_DOC] = magic_comment

# Any content clears the last doc.
            magic_comment = ''

# Simplified YAML specs.
    alldocs[TAG_YAML_SPECS] = '\n'.join(yaml_specs)

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
        name = p.name

        logging.info(f"Doc of {kind}: '{name}'.")


        alldocs = extract_tnsdoc(
            blockname = p.stem,
            content   = p.read_text()
        )

# -- DEBUG - START -- #
        del alldocs[TAG_DOC]

        for k, v in alldocs.items():
            print(f'--- {k} ---')

            if k != TAG_YAML_SPECS:
                v = v[TAG_DOC]

            print(v)

            input('')
# -- DEBUG - END -- #
