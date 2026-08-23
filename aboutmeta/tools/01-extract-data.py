#!/usr/bin/env python3

DEBUG = True
# DEBUG = False


from pathlib import Path
import              sys

TOOLS_DIR = Path(__file__).parent

while TOOLS_DIR.name != "tools":
    TOOLS_DIR = TOOLS_DIR.parent

sys.path.append(str(TOOLS_DIR))

from cbutils.core        import *
from projutils.constants import *


from collections.abc import Iterator


from ruamel.yaml import YAML

ruamel_load = YAML().load


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

def comment_2_tnsdoc(comment):
    lines = [
        x.value.lstrip("# ").rstrip()
        for x in comment
    ]

    comment = '\n'.join(lines)
    comment = comment.strip() + '\n'

    return comment


def extract_metadata(data):
    metadata = dict()

# 1st comments = Main comment + Eventually 1st key comment.
    start_comment = comment_2_tnsdoc(
        data.ca.comment[1]
    )

    print('-- START')
    print(start_comment)
    input('?')

# Key comments for keys.
    for k, v in data.items():
        print(f'-- {k}')

        comment = data.ca.items.get(k, '')

        if comment:
            comment = comment_2_tnsdoc(
                comment[3]
            )

        print(comment)

        input('?')




    exit()











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
a: val-a

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

    print(extract_metadata(data))


exit()















# from ruamel.yaml import YAML
# from ruamel.yaml.comments import CommentedMap, CommentedSeq

# def extract_yaml_structure(node):
#     if isinstance(node, CommentedMap):
#         result = {}

#         # 1. Commentaire de haut de bloc / section (placé sous '..main..')
#         if hasattr(node, "ca") and node.ca.comment and len(node.ca.comment) > 1 and node.ca.comment[1]:
#             main_lines = [t.value.strip() for t in node.ca.comment[1]]
#             result["..main.."] = '\n'.join(main_lines)

#         # 2. Parcours des éléments
#         for key, value in node.items():
#             pre_comments = []
#             inline_comment = None

#             if hasattr(node, "ca") and key in node.ca.items:
#                 comment_info = node.ca.items[key]

#                 # Commentaires au-dessus de la clé
#                 if len(comment_info) > 1 and comment_info[1]:
#                     pre_comments = [t.value.strip() for t in comment_info[1]]

#                 # Commentaire en fin de ligne (inline)
#                 if len(comment_info) > 2 and comment_info[2]:
#                     inline_comment = comment_info[2].value.strip()

#             # Si le sous-élément est un dictionnaire, les commentaires au-dessus deviennent son '..main..'
#             if isinstance(value, CommentedMap):
#                 sub_dict = extract_yaml_structure(value)
#                 if pre_comments:
#                     existing_main = sub_dict.get("..main..", '')
#                     new_main = '\n'.join(pre_comments)
#                     sub_dict["..main.."] = f"{new_main}\n{existing_main}".strip() if existing_main else new_main
#                 result[key] = sub_dict

#             # Pour une valeur simple
#             else:
#                 extracted_val = extract_yaml_structure(value)
#                 all_comments = pre_comments + ([inline_comment] if inline_comment else [])

#                 if all_comments:
#                     result[key] = {
#                         "value": extracted_val,
#                         "..comment..": '\n'.join(all_comments)
#                     }
#                 else:
#                     result[key] = extracted_val

#         return result

#     elif isinstance(node, CommentedSeq):
#         return [extract_yaml_structure(item) for item in node]

#     else:
#         return node

# yaml_text = ''"\
# # Commentaire général en haut du fichier
# # Deuxième ligne du header
# serveur:
#   # Commentaire au-dessus du port
#   port: 8080 # Port HTTP
#   hôte: localhost # Configuration de la base de données

# bdd:
#   nom: app_db
# ''"

# yaml = YAML()
# data = yaml.load(yaml_text)

# res = extract_yaml_structure(data)

# import pprint
# pprint.pprint(res)



# exit()








# ----------- #
# -- TOOLS -- #
# ----------- #






# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

data = dict()

for onedir in CONFIG_DIRS:
    kind = onedir.parent.name

    if kind == 'flavour':
        continue

    subdata = dict()


    logging.info(f"Working on '{kind}'.")

    for p in onedir.glob('*.yaml'):
        logging.info(f"Analysing {kind}: '{p.name}'.")

        this_data = ruamel_load(p.read_text())

        subdata[p.stem] = extract_metadata(this_data)

    data[kind] = subdata


from pprint import pprint

for k, v in data.items():
    print(f'-- {k} --')
    pprint(v)
