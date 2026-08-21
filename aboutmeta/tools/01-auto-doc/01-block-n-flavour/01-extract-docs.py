#!/usr/bin/env python3

from pathlib import Path
import              sys

TOOLS_DIR = Path(__file__).parent

while TOOLS_DIR.name != "tools":
    TOOLS_DIR = TOOLS_DIR.parent

sys.path.append(str(TOOLS_DIR))

from cbutils.core import *


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


MAIN_COMMENT_PATTERN = re.compile(
    r"###\s*\n(.*?)\n\s*###",
    re.DOTALL
)

# - "###\s*\n" : ouverture du bloc
# - "((?:[ \t]*#.*\n)+)" : capture de TOUTES les lignes commençant par # (avec espaces optionnels)
# - "\s*###\s*\n" : fermeture du bloc
# - "([^\n#:]+:[^\n]+)" : capture de la ligne "clé : valeur"
KEY_COMMENT_PATTERN  = re.compile(
    r"###\s*\n((?:[ \t]*#.*\n)+)\s*###\s*\n([^\n#:]+:[^\n]*)",
    re.MULTILINE
)


TAG_MAIN_DOC = "..main.doc.."
TAG_KEY_DOC  = "..key.doc.."
TAG_KEY_VAL  = "..key.val.."


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


def parse_docs(content):
    docs = {}


# Main doc.
    match = MAIN_COMMENT_PATTERN.search(
        content
    )

    if not match:
        raise ValueError('Missing main doc for\n???')

    docs[TAG_MAIN_DOC] = comment_2_doc(
        comment_2_doc(match.group(1))
    )

# Key docs.
    for match in KEY_COMMENT_PATTERN.finditer(content):
        doc    = comment_2_doc(match.group(1))
        key    = match.group(2)
        key, _ = key.split(":", 1)

        docs[key.strip()] = doc

# Nothing left to do
    return docs


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

metada = {}

for onedir in CONFIG_DIRS:
    kind = onedir.parent.name

    logging.info(f"Working on '{kind}'.")
    print(kind)



exit()





# Test
contenu = """
###
# MAIN 1
#
# MAIN 2
#
# MAIN 3
###


###
# SUB 1_1
# SUB 1_2
###
contrib | contribs *:
###
# OK?
###
  subkey: . | list(.)


###
# SUB 2_1
# SUB 2_2
###
keywords *:
  - .

ok: KKK
""".strip()

from pprint import pprint;pprint(parse_docs(contenu))
