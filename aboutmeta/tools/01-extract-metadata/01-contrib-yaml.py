#!/usr/bin/env python3

DEBUG = True
# DEBUG = False


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


from ruamel.yaml import YAML


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

        block.append(line)

        if line == MAGIC_COMMENT_DELIM:
            break

    return block


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
            indent = " " * (len(line) - len(line.lstrip()))

            key, _, val = line.partition(":")
            key, val    = key.strip(), val.strip()

            output.append(f"{indent}{key}:")

            if pending_comment:
                for cl in pending_comment:
                    output.append(f"{indent}  {cl}")

                pending_comment = None

            if val:
                output.append(f"{indent}  {val}")

# Basic lines.
        else:
            output.append(line)

# Nothing left to keep...
    ruamel_content = '\n'.join(output)

    return ruamel_content


# ------------------------------- #
# -- TOOLS - RUAMEL EXTRACTION -- #
# ------------------------------- #

def ruamel_comment_2_tnsdoc(ruamel_comment: str) -> str:
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
    metadata = dict()

# 1st comments = Main comment + Eventually 1st key comment.
    if maindoc:
        comment = ruamel_comment_2_tnsdoc(
            data.ca.comment[1]
        )

        metadata[TAG_MAIN_DOC] = comment

# Key comments for keys.
    for k, v in data.items():
        comment = data.ca.items.get(k, '')

        if comment:
            comment = ruamel_comment_2_tnsdoc(
                comment[3]
            )


        metadata[k] = {
            TAG_SUB_DOC: comment,
            TAG_VAL    :(
                v
                if isinstance(v, str) else
                extract_metadata(v, False)
            ),
        }

# Nothing left to keep...
    return metadata



# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

METADATA = dict()

for onedir in CONFIG_DIRS:
    kind = onedir.parent.name

    if kind == 'flavour':
        continue

    SUB_METADATA = dict()


    logging.info(f"Working on '{kind}'.")

    for p in onedir.glob('*.yaml'):
        logging.info(f"Analysing {kind}: '{p.name}'.")

        data = tnsdoc_2_ruamel(p.read_text())

        print(data)

        SUB_METADATA[p.stem] = extract_metadata(data)

    METADATA[kind] = SUB_METADATA


from pprint import pprint

for k, v in METADATA.items():
    print(f'-- {k} --')
    pprint(v)











# ----------- #
# -- TESTS -- #
# ----------- #

if DEBUG:
    content =  """
###
# T
#
# S'
###


###
# A
###
a: 1234

###
# B
###


b: val-b


###
# C::
#     cccccc
###
c:
  x:
###
# XX
#
# XX
###
    xc: val-xc


###
# IGNORED
###
    """

    print('--- tnsdoc_2_ruamel ---')

    content = tnsdoc_2_ruamel(content)

    print(content)


    print('--- Extract ---')

    data = ruamel_load(content)

    print(repr(extract_metadata(data)))
