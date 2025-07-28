#!/usr/bin/env python3

import                  black
from collections import defaultdict
from datetime    import date
import re

from yaml import (
    safe_load as yaml_load,
    dump      as yaml_dump,
    Dumper
)

from cbdevtools.addfindsrc import addfindsrc
from mistool.os_use        import PPath as Path
from mistool.string_use    import between


# -------------- #
# -- SPEAKING -- #
# -------------- #

TAB_1 = ' '*4
TAB_2 = TAB_1*2
TAB_3 = TAB_1*3


# ------------------- #
# -- AUTO CONTENTS -- #
# ------------------- #

def autoupdate(
    onefile,
    magiccode,
    autocontent
):
    content = onefile.read_text(encoding = 'utf-8')

    before, _ , after = between(
        text = content,
        seps = [
            magiccode,
            magiccode.replace('START', 'END')
        ],
        keepseps = True,
    )

    content = f"{before}\n{autocontent}\n{after.rstrip()}\n\n"

    onefile.write_text(
        data     = content,
        encoding = 'utf-8'
    )


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAG_STATUS = 'status'

ALL_STATUS_TAGS = [
    STATUS_ON_HOLD := 'on hold',
    STATUS_KO      := 'ko',
    STATUS_OK      := 'ok',
    STATUS_UPDATE  := 'update',
]

DEFAULT_STATUS_CONTENT = {
    "status" : STATUS_ON_HOLD,
    "comment": (
        'Specs on hold.'
        ' '
        'The author of jinjaNG will contact you later.'
    )
}


# -------------------------- #
# -- SPECIFIC JSON DUMPER -- #
# -------------------------- #

class IndentDumper(Dumper):
    def increase_indent(
        self,
        flow = False,
        *args, **kwargs
    ):
        return super().increase_indent(
            flow       = flow,
            indentless = False
        )


# ---------------------- #
# -- TOOLS FOR SOURCE -- #
# ---------------------- #

# Specilas chars.
SPECHAR_INSTR   = ':'
SPECHAR_COMMENT = '_'

# Vars
TAG_VAR_START = 'variable_start_string'
# Vars
TAG_VAR_START = 'variable_start_string'
TAG_VAR_END   = 'variable_end_string'
# Instructions.
TAG_BLOCK_INSTR_START = 'block_start_string'
TAG_BLOCK_INSTR_END   = 'block_end_string'
TAG_INLINE_INSTR      = 'line_statement_prefix'
# Comments.
TAG_BLOCK_COMMENT_START = 'comment_start_string'
TAG_BLOCK_COMMENT_END   = 'comment_end_string'
TAG_INLINE_COMMENT      = 'line_comment_prefix'


GRP_TAGS = {
    (TAG_ABOUT:= 'about'): [
        TAG_AUTHOR:= 'author',
        TAG_DESC  := 'desc',
        TAG_DATE  := 'date',
        TAG_UTILS := 'utils',
        TAG_EXTEND:= 'extend',
    ],
    (TAG_SRC_COMMENT:= 'src-comment'): [
        TAG_BLOCK := 'block',
        TAG_INLINE:= 'inline',
    ],
    None: [
        TAG_EXT:= 'ext',
        TAG_VAR:= 'var',
        # TAG_PARAM:= 'param',
    ]
}

TAGS_EXTENDABLE = [
    TAG_UTILS,
    TAG_BLOCK,
    TAG_INLINE,
    TAG_VAR,
]


TAG_1ST_NAME  = '1st name'
TAG_LAST_NAME = 'last name'
TAG_YAML_EMAIL     = 'email'


TAG_JINJA = "jinja2"


def build_extended_flavours(hard_specs_ok):
    for flavour, hardspec in hard_specs_ok.items():
        if not TAG_EXTEND in hardspec[TAG_ABOUT]:
            continue

        extended_fl = hardspec[TAG_ABOUT][TAG_EXTEND]

        if not extended_fl in hard_specs_ok:
            raise Exception(
                f"unknown flavour ''{extended_fl}'' "
                f"to be extended."
            )

        hardspec_to_extend = hard_specs_ok[extended_fl]

        for grptag, subtags in GRP_TAGS.items():
            for tag in subtags:
                if not tag in TAGS_EXTENDABLE:
                    continue

                srctags = (
                    hardspec_to_extend
                    if grptag is None else
                    hardspec_to_extend[grptag]
                )

                if tag in srctags:
                    if grptag is None:
                        if not tag in hardspec:
                            hardspec[tag] = srctags[tag]

                    else:
                        if not grptag in hardspec:
                            hardspec[grptag] = {}

                        if not tag in hardspec[grptag]:
                            hardspec[grptag][tag] = srctags[tag]

        hard_specs_ok[flavour] = hardspec


def build_authorinfos(text):
    firstname, lastname = text.split(',')
    lastname, email = lastname.split('[')

    email = email.strip()[:-1]

    infos = {
        TAG_1ST_NAME : firstname,
        TAG_LAST_NAME: lastname,
        TAG_YAML_EMAIL    : email,
    }

    return {
        k: v.strip()
        for k,v in infos.items()
    }


def build_startend(text):
    start, end = text.split('...')

    return start.strip(), end.strip()


def build_before(text):
    bef, _ = text.split('...')

    return bef.strip()


# # Ici, on change de gestion car on vcréer une regex qui va récupérer just la variable utilisée MYVAR mais aussi tout la commende JNPARAM pour passer à JNVAR(MYVAR) pour la gestion esnsuite par jinja

# def build_paramregex(text):
#     print('TODO >', text)
#     exit()


FORMATERS = {
    TAG_AUTHOR: build_authorinfos,
    TAG_BLOCK : build_startend,
    TAG_INLINE: build_before,
    TAG_VAR   : build_startend,
    # TAG_PARAM : build_paramregex,
}


def specs2options(hardspec):
    options = {}

    for grptag, subtags in GRP_TAGS.items():
        if grptag is None:
            dict2use = hardspec.copy()

        else:
            dict2use = hardspec[grptag]

        for tag, val in dict2use.items():
            if not tag in subtags:
                raise Exception(
                    f"unknown key: {tag}.")

            if tag in FORMATERS:
                val = FORMATERS[tag](val)

            options[tag] = val

            if grptag is None:
                del hardspec[tag]

        if not grptag is None:
            del hardspec[grptag]

    options[TAG_UTILS] = options.get(TAG_UTILS, False)

    return options


# ---------------------- #
# -- TOOLS FOR SOURCE -- #
# ---------------------- #

CODE_SETTINGS_TEMPL = """
{about}

ASSOCIATED_EXT[FLAVOUR_{name_up}] = {autoext}

WITH_UTILS[FLAVOUR_{name_up}] = {withutils}

JINJA_TAGS[FLAVOUR_{name_up}] = {forjinja}

""".lstrip()


def build_all_settings(options):
    if not TAG_VAR in options:
        raise Exception('Missing var...')

    autoext = [
        p
        if p == "*" else
        f"*.{p}"
        for p in options[TAG_EXT]
    ]

    withutils = options[TAG_UTILS]

    forjinja = {
        TAG_VAR_START: options[TAG_VAR][0],
        TAG_VAR_END  : options[TAG_VAR][1],
    }

    if not(
        TAG_BLOCK in options
        or
        TAG_INLINE in options
    ):
        raise Exception('No comment!')

    if TAG_INLINE in options:
        forjinja[TAG_INLINE_COMMENT] = options[TAG_INLINE] + SPECHAR_COMMENT
        forjinja[TAG_INLINE_INSTR]   = options[TAG_INLINE] + SPECHAR_INSTR

    if TAG_BLOCK in options:
        block_start, block_end = options[TAG_BLOCK]

        if not TAG_INLINE in options:
            forjinja[TAG_INLINE_COMMENT] = None
            forjinja[TAG_INLINE_INSTR]   = None

    else:
        block_start = block_end = options[TAG_INLINE] + options[TAG_INLINE][-1]

    forjinja[TAG_BLOCK_COMMENT_START] = block_start + SPECHAR_COMMENT
    forjinja[TAG_BLOCK_COMMENT_END]   = SPECHAR_COMMENT + block_end

    forjinja[TAG_BLOCK_INSTR_START] = block_start + SPECHAR_INSTR
    forjinja[TAG_BLOCK_INSTR_END]   = SPECHAR_INSTR + block_end


    return forjinja, withutils, autoext


def asciititle(title):
    deco = '-'*(2*3 + len(title))

    return f"""
# {deco} #
# -- {title.upper()} -- #
# {deco} #
    """.strip()


def build_src(name, options, autofromext):
    date   = options[TAG_DATE]
    author = options[TAG_AUTHOR]
    author = (
          author[TAG_1ST_NAME]
        + " " +
          author[TAG_LAST_NAME]
    )

    about = f"""
{asciititle(name)}
#
# {options[TAG_DESC]}
#
# Last change: {date}
# Author     : {author}
    """.strip()

    forjinja, withutils, autoext = build_all_settings(options)

    autofromext[name] = set(autoext)

    pycode = CODE_SETTINGS_TEMPL.format(
        name      = name,
        name_up   = name.upper(),
        about     = about,
        withutils = withutils,
        forjinja  = forjinja,
        autoext   = autoext,
    )

    return pycode
