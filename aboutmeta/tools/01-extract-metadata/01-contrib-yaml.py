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


from ruamel.yaml          import YAML
from ruamel.yaml.comments import (
    CommentedSeq,
    CommentedMap,
)


# ---------------------- #
# -- RUAMEL SAFE MODE -- #
# ---------------------- #

from ruamel.yaml.constructor import RoundTripConstructor

class AllStrRoundTripConstructor(RoundTripConstructor):
    pass

def construct_yaml_str(self, node):
    return self.construct_scalar(node)

for tag in (
    'tag:yaml.org,2002:int',
    'tag:yaml.org,2002:float',
    'tag:yaml.org,2002:bool',
    'tag:yaml.org,2002:timestamp',
    'tag:yaml.org,2002:null',
):
    AllStrRoundTripConstructor.add_constructor(tag, construct_yaml_str)

yaml = YAML(typ='rt')
yaml.Constructor = AllStrRoundTripConstructor

ruamel_load = yaml.load


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


# ----------------------------- #
# -- TOOLS - RUAMEL FRIENDLY -- #
# ----------------------------- #

def tnsdoc_2_ruamel(content: str) -> (str, str):
    lines_iter = iter(content.strip().splitlines())

# Main mandatory doc extraction.
    line = next(lines_iter)

    if line != MAGIC_COMMENT_DELIM:
        raise ValueError('Missing mandatory main doc via magic comment')

    main_doc = comment_2_tnsdoc(
        '\n'.join(
            extract_magic_comment(lines_iter)
        )
    )

# Let's prepare other magic comments for ruamel.
    output          = []
    pending_comment = None

    for line in lines_iter:
# One new magic comment.
        if line.rstrip() == MAGIC_COMMENT_DELIM:
            magic_comment = extract_magic_comment(lines_iter)

            if not output:
                output.extend(magic_comment)

            else:
                pending_comment = magic_comment

            continue
# YAML key/val.
        if ":" in line:
            indent = get_indent(line)

            key, _, val = line.partition(":")
            key, val    = key.strip(), val.strip()

            output.append(f"{indent}{key}:")

            indent += ' '*2

            add_comment(
                output          = output,
                pending_comment = pending_comment,
                indent          = indent,
            )

            pending_comment = None

            if val:
                output.append(f"{indent}{val}")

# YAML list.
        elif (
            line
            and
            line.lstrip()[0] == '-'
        ):
            indent = get_indent(line)

            add_comment(
                output          = output,
                pending_comment = pending_comment,
                indent          = indent,
            )

            pending_comment = None

            output.append(line)

# Basic lines.
        else:
            output.append(line)

# Nothing left to keep...
    ruamel_content = '\n'.join(output)
    ruamel_content = ruamel_content.strip()

    return main_doc, ruamel_content


def extract_magic_comment(line_iter : Iterator[str]) -> list[str]:
    block = [MAGIC_COMMENT_DELIM]

    for line in line_iter:
        line = line.strip()

        if(
            not line
            or
            line[0] != '#'
        ):
            raise ValueError('Illegal magic comment!')

        block.append(line)

        if line == MAGIC_COMMENT_DELIM:
            break

    if(
        len(block) == 1
        or
        block[-1] != MAGIC_COMMENT_DELIM
    ):
        raise ValueError('Illegal magic comment!')

    return block


def get_indent(line: str) -> str:
    return " " * (len(line) - len(line.lstrip()))


def add_comment(
    output         : list[str],
    pending_comment: list[str],
    indent         : str,
) -> None :
    if pending_comment:
        for cl in pending_comment:
            output.append(f"{indent}{cl}")


# ------------------------------- #
# -- TOOLS - RUAMEL EXTRACTION -- #
# ------------------------------- #

def extract_metadata(data: dict[str]) -> dict[str]:
    TODO



# Nothing to do.
    if isinstance(data, str):
        return data

# We have some work to do.
    metadata = dict()

# Case 1: dict
    if isinstance(data, CommentedMap):
        submetadata = dict()

        for k, v in data.items():
            submetadata[k] = dict()

            comment = data.ca.items.get(k, '')

            if comment:
                comment = ruamel_comment_2_tns(comment[3])

                if comment:
                    submetadata[k][TAG_DOC] = comment

            v = extract_metadata(v)

            submetadata[k] |= {
                TAG_IS_LOF: False,
                TAG_DATA  : v,
            }


        metadata[TAG_DATA] = submetadata

# Case 2: list
    elif isinstance(data, CommentedSeq):
        metadata[TAG_DATA] = {
            TAG_IS_LOF: True,
            TAG_VAL   : data[0],
        }

# Case 3: unsupported type
    else:
        raise TypeError(
             "Only dicts and lists are supporetd."
             "\n"
            f"  > Type : '{type(data)}'"
             "\n"
            f"  > Value: '{data}'"
        )

# Nothing left to keep...
    return metadata


def ruamel_comment_2_tns(ruamel_comment: None | list[Any]) -> str:
    if ruamel_comment is None:
        return ''

    return comment_2_tnsdoc(
            '\n'.join([
            x.value
            for x in ruamel_comment
        ])
    )


# -- DEBUG - START -- #
content =  """
###
# MAIN
###
a:
###
# X
# X
###
  x:ok
"""

# content =  """
# ###
# # MAIN
# #
# #DOC
# ###

# ###
# # A
# ###
# - a
# """

# content =  """
# ###
# # MAIN
# #
# #DOC
# ###

# ###
# # A
# ###
# a:
#   - b
# """

# content =  """
# ###
# # MAIN
# #
# #DOC
# ###

# ###
# # A
# ###
# a:
#   - b
# """

print('--- tnsdoc_2_ruamel ---')
maindoc, content = tnsdoc_2_ruamel(content)
print(maindoc)
print('~~~')
print('~~~')
print(content)
print('--- data ---')
data = ruamel_load(content)
print(type(data))
print(repr(data))
print('--- Extract ---')
from pprint import pprint
pprint(extract_metadata(data))
exit()
# -- DEBUG - END -- #


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
        logging.info(f"Analysing {kind}: '{p.name}'.")

        maindoc, content = tnsdoc_2_ruamel(content = p.read_text())

        data = ruamel_load(content)

        SUB_METADATA[p.stem] = {
            TAG_MAIN_DOC: maindoc,
            TAG_DATA    : extract_metadata(data = data),
        }

    METADATA[kind] = SUB_METADATA

# -- DEBUG - START -- #
from pprint import pprint;pprint(METADATA)
# -- DEBUG - END -- #
