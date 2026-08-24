#!/usr/bin/env python3

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

def _extract_block(line_iter : Iterator[str]) -> list[str]:
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


def tnsdoc_2_ruamel(content: str) -> str:
    lines_iter      = iter(content.strip().splitlines())
    output          = []
    pending_comment = None

    for line in lines_iter:
        line = line.rstrip()

# Magic comments.
        if line == MAGIC_COMMENT_DELIM:
            block = _extract_block(lines_iter)

            if not output:
                output.extend(block)

            else:
                pending_comment = block

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

    return ruamel_content


# ------------------------------- #
# -- TOOLS - RUAMEL EXTRACTION -- #
# ------------------------------- #

def ruamel_comment_2_tns(ruamel_comment: str) -> str:
    if ruamel_comment is None:
        return ''

    comment = comment_2_tnsdoc(
        '\n'.join([
            x.value
            for x in ruamel_comment
        ])
    )

    comment = comment.strip()

    return comment


def extract_metadata(
    data   : dict[str],
    maindoc: bool = True
 ) -> dict[str]:
# Nothing to do.
    if isinstance(data, str):
        return data

# We have some work to do.
    metadata = dict()

# 1st comments = Main comment + Eventually 1st key comment.
    if maindoc:
        comment = ruamel_comment_2_tns(
            data.ca.comment[1]
        )

        metadata[TAG_MAIN_DOC] = comment

# Case 1: dict
    if isinstance(data, CommentedMap):
        metadata[TAG_TYPE] = TAG_DICT

        submetadata = dict()

        for k, v in data.items():
            comment = data.ca.items.get(k, '')

            if comment:
                comment = ruamel_comment_2_tns(comment[3])

            v = extract_metadata(
                data    = v,
                maindoc = False,
            )

            submetadata[k] = {
                TAG_DOC: comment,
                TAG_VAL: v,
            }

        metadata[TAG_VAL] = submetadata

# Case 2: list
    elif isinstance(data, CommentedSeq):
        metadata[TAG_TYPE] = TAG_LIST

        comment = data.ca.comment

        if comment:
            comment = ruamel_comment_2_tns(comment[1])

        else:
            comment = ''

        metadata[TAG_VAL] = {
            TAG_DOC: comment,
            TAG_VAL: data,
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


# -- DEBUG - START -- #
# content =  """
# ###
# # A
# ###
# a:
# ###
# # C
# # C
# # C
# # C
# ###
#   - c
# """
content =  """
###
# A
###

###
# B
###
- a
"""
print('--- tnsdoc_2_ruamel ---')
content = tnsdoc_2_ruamel(content)
print(content)
print('--- data ---')
data = ruamel_load(content)
print(type(data))
print(repr(data))
print('--- Extract ---')
print(repr(extract_metadata(data)))
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

        data = ruamel_load(
            tnsdoc_2_ruamel(content = p.read_text())
        )

        SUB_METADATA[p.stem] = extract_metadata(data = data)

    METADATA[kind] = SUB_METADATA

# -- DEBUG - START -- #
from pprint import pprint;pprint(METADATA)
# -- DEBUG - END -- #
