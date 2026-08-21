#!/usr/bin/env python3

from pathlib import Path
import              sys

TOOLS_DIR = Path(__file__).parent

while TOOLS_DIR.name != "tools":
    TOOLS_DIR = TOOLS_DIR.parent

sys.path.append(str(TOOLS_DIR))

from cbutils.core        import *
from projutils.constants import *

from ruamel.yaml import YAML

ruamel_load = YAML().load


























# from ruamel.yaml import YAML
# from ruamel.yaml.comments import CommentedMap, CommentedSeq

# def extract_yaml_structure(node):
#     if isinstance(node, CommentedMap):
#         result = {}

#         # 1. Commentaire de haut de bloc / section (placé sous '..main..')
#         if hasattr(node, "ca") and node.ca.comment and len(node.ca.comment) > 1 and node.ca.comment[1]:
#             main_lines = [t.value.strip() for t in node.ca.comment[1]]
#             result["..main.."] = "\n".join(main_lines)

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
#                     existing_main = sub_dict.get("..main..", "")
#                     new_main = "\n".join(pre_comments)
#                     sub_dict["..main.."] = f"{new_main}\n{existing_main}".strip() if existing_main else new_main
#                 result[key] = sub_dict

#             # Pour une valeur simple
#             else:
#                 extracted_val = extract_yaml_structure(value)
#                 all_comments = pre_comments + ([inline_comment] if inline_comment else [])

#                 if all_comments:
#                     result[key] = {
#                         "value": extracted_val,
#                         "..comment..": "\n".join(all_comments)
#                     }
#                 else:
#                     result[key] = extracted_val

#         return result

#     elif isinstance(node, CommentedSeq):
#         return [extract_yaml_structure(item) for item in node]

#     else:
#         return node

# yaml_text = """\
# # Commentaire général en haut du fichier
# # Deuxième ligne du header
# serveur:
#   # Commentaire au-dessus du port
#   port: 8080 # Port HTTP
#   hôte: localhost # Configuration de la base de données

# bdd:
#   nom: app_db
# """

# yaml = YAML()
# data = yaml.load(yaml_text)

# res = extract_yaml_structure(data)

# import pprint
# pprint.pprint(res)



# exit()





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


print(TAG_MAIN_DOC)

exit()






# ----------- #
# -- TOOLS -- #
# ----------- #

def normalize(data):
# 1st comments = Main comment + Eventually 1st key comment.
    start_comment = ruamel_comment_2_content(
        data.ca.comment[1]
    )

    print('-- START')
    print('')
    print(start_comment)
    input('?')

# Key comments for keys.
    for k, v in data.items():
        print(f'-- {k}')

        comment = data.ca.items.get(k, '')

        if comment:
            comment = ruamel_comment_2_content(
                comment[3]
            )

        print('')
        print(comment)

        input('?')




    exit()


def ruamel_comment_2_content(ruamel_comment):
    return '\n'.join(
        x.value.strip()
        for x in ruamel_comment
    )

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

    if kind == 'flavour':
        continue

    subdata = dict()


    logging.info(f"Working on '{kind}'.")

    for p in onedir.glob('*.yaml'):
        logging.info(f"Analysing {kind}: '{p.name}'.")

        this_data = ruamel_load(p.read_text())

        subdata[p.stem] = normalize(this_data)

    data[kind] = subdata


from pprint import pprint

for k, v in data.items():
    print(f'-- {k} --')
    pprint(v)
