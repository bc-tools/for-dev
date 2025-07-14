#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project “black.”    -- #
# ------------------------------------------------------- #


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAG_ALT_ALL = "__alternative_all__"
TAG_ALT_TUPLES = "__alternative_tuples__"
TAG_BLOCK = "__block__"
TAG_DATA = "__data__"
TAG_LIST_OF = "__list_of__"
TAG_PARSER = "__parser__"
TAG_REQUIRED = "__required__"
TAG_TYPE = "__type__"

TAG_PARSER_LANG = "lang"
TAG_PARSER_LICENSE = "license"
TAG_PARSER_PATH = "path"
TAG_PARSER_PERSON = "person"
TAG_PARSER_VERSION = "version"


# ------------------------ #
# -- READY-TO-USE SPECS -- #
# ------------------------ #

YAML_SPECS = {
    "project": {
        TAG_ALT_ALL: (),
        "project": {
            TAG_REQUIRED: False,
            TAG_TYPE: TAG_BLOCK,
            TAG_ALT_ALL: ("authors", "author", "contribs", "contrib"),
            TAG_ALT_TUPLES: (("authors", "author"), ("contribs", "contrib")),
            TAG_PARSER_VERSION: {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_DATA,
                TAG_LIST_OF: False,
                TAG_PARSER: TAG_PARSER_VERSION,
            },
            "acronym": {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_DATA,
                TAG_LIST_OF: False,
                TAG_PARSER: None,
            },
            "codename": {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_DATA,
                TAG_LIST_OF: False,
                TAG_PARSER: None,
            },
            "desc": {
                TAG_REQUIRED: True,
                TAG_TYPE: TAG_DATA,
                TAG_LIST_OF: False,
                TAG_PARSER: None,
            },
            "authors": {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_DATA,
                TAG_LIST_OF: True,
                TAG_PARSER: TAG_PARSER_PERSON,
            },
            "author": {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_DATA,
                TAG_LIST_OF: False,
                TAG_PARSER: TAG_PARSER_PERSON,
            },
            "contribs": {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_DATA,
                TAG_LIST_OF: True,
                TAG_PARSER: TAG_PARSER_PERSON,
            },
            "contrib": {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_DATA,
                TAG_LIST_OF: False,
                TAG_PARSER: TAG_PARSER_PERSON,
            },
            "urls": {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_BLOCK,
                TAG_ALT_ALL: (),
                "home": {
                    TAG_REQUIRED: False,
                    TAG_TYPE: TAG_DATA,
                    TAG_LIST_OF: False,
                    TAG_PARSER: None,
                },
                "dev": {
                    TAG_REQUIRED: False,
                    TAG_TYPE: TAG_DATA,
                    TAG_LIST_OF: False,
                    TAG_PARSER: None,
                },
                "issues": {
                    TAG_REQUIRED: False,
                    TAG_TYPE: TAG_DATA,
                    TAG_LIST_OF: False,
                    TAG_PARSER: None,
                },
            },
            "licenses": {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_BLOCK,
                TAG_ALT_ALL: (),
                "code": {
                    TAG_REQUIRED: False,
                    TAG_TYPE: TAG_DATA,
                    TAG_LIST_OF: False,
                    TAG_PARSER: TAG_PARSER_LICENSE,
                },
                "manual": {
                    TAG_REQUIRED: False,
                    TAG_TYPE: TAG_DATA,
                    TAG_LIST_OF: False,
                    TAG_PARSER: TAG_PARSER_LICENSE,
                },
            },
            "langs": {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_BLOCK,
                TAG_ALT_ALL: (),
                "doc": {
                    TAG_REQUIRED: False,
                    TAG_TYPE: TAG_DATA,
                    TAG_LIST_OF: False,
                    TAG_PARSER: TAG_PARSER_LANG,
                },
                "manual": {
                    TAG_REQUIRED: False,
                    TAG_TYPE: TAG_DATA,
                    TAG_LIST_OF: False,
                    TAG_PARSER: TAG_PARSER_LANG,
                },
            },
            "require": {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_DATA,
                TAG_LIST_OF: True,
                TAG_PARSER: None,
            },
            "keywords": {
                TAG_REQUIRED: False,
                TAG_TYPE: TAG_DATA,
                TAG_LIST_OF: True,
                TAG_PARSER: None,
            },
        },
    },
    "toc": {
        TAG_ALT_ALL: (),
        "toc": {
            TAG_REQUIRED: False,
            TAG_TYPE: TAG_DATA,
            TAG_LIST_OF: True,
            TAG_PARSER: TAG_PARSER_PATH,
        },
    },
}
