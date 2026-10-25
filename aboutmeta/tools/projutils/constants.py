#!/usr/bin/env python3


# --------------------- #
# -- FORM YAML SPECS -- #
# --------------------- #

TAG_POST_PROCESS = '+'
TAG_OPTIONAL     = '*'
TAG_PIP          = '|'
TAG_COMMA        = ','


TAG_LAST_PARSER_CARD = '.'


TAG_IS_MANDATORY = "__IS_MANDATORY__"
TAG_IS_PARSED    = "__IS_PARSED__"
TAG_ALTS         = "__ALTERNATIVES__"

DATA_TYPES_ALLOWED =[
    TAG_LIST:= "list",
    TAG_DATA:= "data",
]


TAG_STR = "str"
