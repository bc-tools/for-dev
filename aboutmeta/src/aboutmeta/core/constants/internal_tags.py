#!/usr/bin/env python3


# ---------- #
# -- FILE -- #
# ---------- #

TAG_PATH_SEP   = '/'
TAG_ABOUT_YAML = 'about.yaml'


# ---------- #
# -- DATA -- #
# ---------- #

TAG_DATATYPE = '__DATATYPE__'

ALL_AMDTAGS_DATATYPES = [
    TAG_LIST := '__LIST__',
    TAG_DATA := '__DATA__',
]

TAG_PARSER     = '__PARSER__'
TAG_USE_POST   = '__USE_POST__'
TAG_AMDATA_USE = '__AMDATA_USE__'


# ------------ #
# -- BLOCKS -- #
# ------------ #

TAG_ALTERNATIVES = '__ALTERNATIVES__'

SPECIAL_KEYS = set([
    TAG_IS_MANDATORY := '__IS_MANDATORY__',
    TAG_IS_PARSED    := '__IS_PARSED__',
])

TAG_BLOCK_PARSERS = '__BLOCK_PARSERS__'
TAG_BLOCK_STATUS  = '__BLOCK_STATUS__'
TAG_BLOCK_ALTS    = '__BLOCK_ALTS__'


# -------------- #
# -- FLAVOURS -- #
# -------------- #

TAG_PATH_OPTIONAL = '*'
