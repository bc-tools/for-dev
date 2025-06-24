#!/usr/bin/env python3

from btools.B01 import *


addfindsrc(
    file    = __file__,
    project = 'jinjaNG',
)

from src.config.jngflavours import *


# ! -- DEBUGGING -- ! #
# Clear the terminal.
# print("\033c", end="")
# ! -- DEBUGGING -- ! #


# --------------- #
# -- CONSTANTS -- #
# --------------- #

FORCE_TOC_UPDATE = False
# FORCE_TOC_UPDATE = True


THIS_FILE = Path(__file__)
THIS_DIR  = Path(THIS_FILE).parent

PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'jinjaNG'):
   PROJECT_DIR = PROJECT_DIR.parent

THIS_FILE_REL_SRC_PATH    = Path(__file__) - PROJECT_DIR
THIS_FILE_REL_PROJECT_DIR = THIS_FILE - PROJECT_DIR


DOC_DIR               = PROJECT_DIR / 'doc' / 'content'
SPECS_CONTENT_TNSFILE = DOC_DIR / 'specs.txt'
SPECS_DOC_DIR         = DOC_DIR / 'specs'


DEFAULT_TEMPLATES = {
    (TAG_VARS:= 'variables'): """
this::
    date = ?


========================
Variables dans un patron
========================

TODO

/* Contenu de base.

Les variables se tapent comme dans l'exemple suivant.

jinjang::
    ---
    flavour = {flavour}
    ---

    J'utilise une variable : {variable_start_string} une_var {variable_end_string}.
*/
    """,
    (TAG_INSTR:= 'instructions'): """
this::
    date = ?


==============================
Instructions du langage ¨jinja
==============================

TODO

/* Contenu de base.

Voici comment utiliser des intructions ¨jinja sur une ligne, ou dans un bloc.

jinjang::
    ---
    flavour = {flavour}
    ---

    inline::{line_statement_prefix} varloc = 100

    Compte de 10 en 10 de 10 à {variable_start_string} varlocale {variable_end_string}.

    {block_start_string} for i in range(10,
                       varlocale + 1,
                       10) {block_end_string}
        * {{ i }}
    {block_start_string} endfor {block_end_string}
*/
    """,
    (TAG_COMMENT:= 'comments'): """
this::
    date = ?


====================
Commenter son patron
====================

TODO

/* Contenu de base.

Deux types de commentaire sont disponibles.

jinjang::
    ---
    flavour = {flavour}
    ---

    inline::{line_comment_prefix} Un commentaire sur une seule ligne.

    {block_start_string} Un commentaire
        sur
        plusieurs lignes. {block_end_string}
*/
    """,
    TAG_UTILS: """
this::
    date = ?


=============================
Outils d'aide à la conception
=============================

TODO

/* Contenu de base.

EXplications sur les outils proposés... A vous de jouer !
*/
    """,
    (TAG_LISTEXT:= 'extensions'): """
this::
    date = {date}


{title}

<:explanations:> à la saveur ''{flavour}''<:extra:>.

/* -- AUTO LIST - START -- */
/* -- AUTO LIST - END -- */
    """,
}


# ----------- #
# -- TOOLS -- #
# ----------- #

def tnstitle(title):
    deco  = '='*len(title)

    return f'{deco}\n{title}\n{deco}'


DATE_PATTERN       = re.compile(r"\s+date\s*=.*")
DECO_TITLE_PATTERN = re.compile(r"={3,}")


INLINE_     = f"inline::"
INLINE_NONE = f"{INLINE_}None "

def build_predoc(flavour, filename):
    predoc = DEFAULT_TEMPLATES[filename].format(
        flavour = flavour,
        **JINJA_TAGS[flavour]
    )

# No inline ?
    if not INLINE_NONE in predoc:
        predoc = predoc.replace(INLINE_, '')

    else:
        newpredoc = []

        for line in predoc.split('\n'):
            if INLINE_NONE in line:
                before, after = line.split(INLINE_NONE)

                line = (
                      before
                    + JINJA_TAGS[flavour][TAG_BLOCK_INSTR_START]
                    + ' '
                    + after
                    + ' '
                    + JINJA_TAGS[flavour][TAG_BLOCK_INSTR_END]
                )

            newpredoc.append(line)

        predoc = '\n'.join(newpredoc)

    return predoc


TEMPL_TOC = """
abbrev::
    content = /{flavour}


{title}

content::
    {toc}
""".strip()


def build_toc(flavour):
    toc = []

    for p in DEFAULT_FILES:
        if(
            p.stem == TAG_UTILS
            and
            not WITH_UTILS[flavour]
        ):
            continue

        toc.append(f'¨content/{p.name}')

    toc = ('\n' + ' '*4).join(toc)

    title = f"La saveur ''{flavour}''"

    return TEMPL_TOC.format(
        flavour = flavour,
        title   = tnstitle(title),
        toc     = toc,
    )


ACTION_ADDING   = "adding"
ACTION_UPDATING = "updating"
ACTION_NOTHING  = ""


def build_ext(flavour, autoext, dest_file):
    today = date.today()

# Content
    if dest_file.is_file():
        action  = ACTION_UPDATING
        content = dest_file.read_text(encoding = 'utf-8')

    else:
        action = ACTION_ADDING

        title = f"Fichiers ¨auto^t associés à la saveur ''{flavour}''"

        content = DEFAULT_TEMPLATES[TAG_LISTEXT].format(
            date    = today,
            title   = tnstitle(title),
            flavour = flavour,
        )

# Last extensions
    before, lastext , after = between(
        text = content,
        seps = [
            '/* -- AUTO LIST - START -- */',
            '/* -- AUTO LIST - END -- */'
        ],
        keepseps = True,
    )

    lastext = extract_lastext(lastext)
    newext  = autoext

    if same_ext(lastext, newext):
        return ACTION_NOTHING

# Some new extensions
    if action == ACTION_ADDING:
        if len(newext) == 1:
            explanations = "Un seul type de fichier est automatiquement associé"
            extra        = ""

        else:
            explanations = "Voici les types de fichier automatiquement associés"
            extra        =" (la recherche se fait dans l'ordre indiquée, et s'arrête dès la première concordance trouvée)"

        before = before.replace(
            "<:explanations:>",
            explanations
        ).replace(
            "<:extra:>",
            extra
        )

    newext = [
        ' '*4 + f"* path::''{e}''"
        for e in newext
    ]
    newext = '\n'.join(newext)

# Uodating the date
    if action == ACTION_UPDATING:
        newbefore = []

        for line in before.split('\n'):
            if re.match(DATE_PATTERN, line):
                line = ' '*4 + f"date = {today}"

            newbefore.append(line)

        before = '\n'.join(newbefore)

# New content.
    content = dest_file.write_text(
        data     = f"{before}\n{newext}\n{after}",
        encoding = 'utf-8'
    )

# All job done.
    return action


def extract_lastext(lastext):
    listext = []

    for line in lastext.split('\n'):
        line = line.strip()

        if line:
            line = line[1:].strip()

        for toremove in [
            "path::",
            "''"
        ]:
            line = line.replace(toremove, "")

        if line:
            listext.append(line)

    return listext


def same_ext(lastext, newext):
    l_1 = lastext.copy()
    l_1.sort()

    l_2 = newext.copy()
    l_2.sort()

    return l_1 == l_2


# ---------------------------- #
# -- PREPARING THE CONTENTS -- #
# ---------------------------- #

MAIN_TOC = []

for flavour in sorted(ASSOCIATED_EXT):
    if flavour == FLAVOUR_ASCII:
        continue

    MAIN_TOC.append(flavour)

    print(f'{TAB_1}* Missing doc for the flavour ''{flavour}''?')

    nothingdone = True

# The contents
    autoext  = ASSOCIATED_EXT[flavour]
    dest_dir = SPECS_DOC_DIR / flavour

    for filename in DEFAULT_TEMPLATES:
        dest_file = dest_dir / f"{filename}.txt"

        if filename == TAG_LISTEXT:
            action = build_ext(flavour, autoext, dest_file)

            if action:
                print(
                    f"{TAB_2}+ {action.title()} the file ''{filename}''."
                )

            continue

        if dest_file.is_file():
            continue

        if (
            filename == TAG_UTILS
            and
            WITH_UTILS[flavour] == False
        ):
            continue

        nothingdone = False

        print(f"{TAB_2}+ Adding the file ''{filename}''.")

        predoc = build_predoc(flavour, filename)

        dest_file.create('file')
        dest_file.write_text(
            data     = predoc,
            encoding = 'utf-8'
        )


# TOC
    tocfile = SPECS_DOC_DIR / f"{flavour}.txt"

    if FORCE_TOC_UPDATE or not tocfile.is_file():
        nothingdone = False

        print(f"{TAB_2}+ TOC - Adding ''{flavour}.txt''.")

        toc = build_toc(flavour)

        tocfile.touch()
        tocfile.write_text(
            data     = toc,
            encoding = 'utf-8'
        )


    if nothingdone:
        print(f"{TAB_2}+ No file added.")


# ----------------------------------------- #
# -- UPDATING THE TOC OF MAIN SPECS FILE -- #
# ----------------------------------------- #

print(f'{TAB_1}* Updating the TOC for all the flavours.')

content = SPECS_CONTENT_TNSFILE.read_text(encoding = 'utf-8')

before, _ , after = between(
    text = content,
    seps = [
        '/* -- AUTO CONTENT - START -- */',
        '/* -- AUTO CONTENT - END -- */'
    ],
    keepseps = True,
)

toc = [' '*4 + f'¨content/{f}.txt' for f in MAIN_TOC]
toc = '\n'.join(toc)

SPECS_CONTENT_TNSFILE.write_text(
    data     = f"{before}\n{toc}\n{after}",
    encoding = 'utf-8'
)
