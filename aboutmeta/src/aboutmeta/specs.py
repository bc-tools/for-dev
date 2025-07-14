#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project “black.”    -- #
# ------------------------------------------------------- #

# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAG_SPECS_ALT_ALL = "ALT_ALL"
TAG_SPECS_ALT_TUPLES = "ALT_TUPLES"
TAG_SPECS_BLOCK = "BLOCK"
TAG_SPECS_CONTENT = "CONTENT"
TAG_SPECS_DATA = "DATA"
TAG_SPECS_LIST_OF = "LIST_OF"
TAG_SPECS_PARSER = "PARSER"
TAG_SPECS_REQUIRED = "REQUIRED"
TAG_SPECS_TYPE = "TYPE"

TAG_SPECS_PARSER_LANG = "lang"
TAG_SPECS_PARSER_LICENSE = "license"
TAG_SPECS_PARSER_PATH = "path"
TAG_SPECS_PARSER_PERSON = "person"
TAG_SPECS_PARSER_VERSION = "version"


# ------------------------ #
# -- READY-TO-USE SPECS -- #
# ------------------------ #

SPECS_PARSING = {
    TAG_SPECS_ALT_ALL: (),
    "project": {
        TAG_SPECS_REQUIRED: False,
        TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
        TAG_SPECS_CONTENT: {
            TAG_SPECS_ALT_ALL: ("authors", "author", "contribs", "contrib"),
            TAG_SPECS_ALT_TUPLES: (("authors", "author"), ("contribs", "contrib")),
            TAG_SPECS_PARSER_VERSION: {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: TAG_SPECS_PARSER_VERSION,
            },
            "acronym": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: None,
            },
            "codename": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: None,
            },
            "desc": {
                TAG_SPECS_REQUIRED: True,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: None,
            },
            "authors": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: True,
                TAG_SPECS_PARSER: TAG_SPECS_PARSER_PERSON,
            },
            "author": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: TAG_SPECS_PARSER_PERSON,
            },
            "contribs": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: True,
                TAG_SPECS_PARSER: TAG_SPECS_PARSER_PERSON,
            },
            "contrib": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: TAG_SPECS_PARSER_PERSON,
            },
            "urls": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
                TAG_SPECS_CONTENT: {
                    TAG_SPECS_ALT_ALL: (),
                    "home": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: None,
                    },
                    "dev": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: None,
                    },
                    "issues": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: None,
                    },
                },
            },
            "licenses": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
                TAG_SPECS_CONTENT: {
                    TAG_SPECS_ALT_ALL: (),
                    "code": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: TAG_SPECS_PARSER_LICENSE,
                    },
                    "manual": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: TAG_SPECS_PARSER_LICENSE,
                    },
                },
            },
            "langs": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
                TAG_SPECS_CONTENT: {
                    TAG_SPECS_ALT_ALL: (),
                    "doc": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: TAG_SPECS_PARSER_LANG,
                    },
                    "manual": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: TAG_SPECS_PARSER_LANG,
                    },
                },
            },
            "require": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: True,
                TAG_SPECS_PARSER: None,
            },
            "keywords": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: True,
                TAG_SPECS_PARSER: None,
            },
        },
    },
    "toc": {
        TAG_SPECS_REQUIRED: False,
        TAG_SPECS_TYPE: TAG_SPECS_DATA,
        TAG_SPECS_LIST_OF: True,
        TAG_SPECS_PARSER: TAG_SPECS_PARSER_PATH,
    },
}
