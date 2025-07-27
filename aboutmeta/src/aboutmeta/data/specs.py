#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
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
TAG_SPECS_POST_PROD = "POST-PROD"
TAG_SPECS_PARSER = "PARSER"
TAG_SPECS_REQUIRED = "REQUIRED"
TAG_SPECS_TYPE = "TYPE"

TAG_PARSER_DATE = "date"
TAG_PARSER_LANG = "lang"
TAG_PARSER_LICENSE = "license"
TAG_PARSER_PERSON = "person"
TAG_PARSER_STR = "str"
TAG_PARSER_TOCPATH = "tocpath"
TAG_PARSER_URL = "url"
TAG_PARSER_VERSION = "version"


# ------------------------ #
# -- READY-TO-USE SPECS -- #
# ------------------------ #

SPECS = {
    TAG_SPECS_ALT_ALL: (),
    "project": {
        TAG_SPECS_REQUIRED: False,
        TAG_SPECS_POST_PROD: False,
        TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
        TAG_SPECS_CONTENT: {
            TAG_SPECS_ALT_ALL: (
                "author",
                "authors",
                "codename",
                "contrib",
                "contribs",
                "doctitle",
            ),
            TAG_SPECS_ALT_TUPLES: (
                ("author", "authors"),
                ("codename", "doctitle"),
                ("contrib", "contribs"),
            ),
            "version": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: TAG_PARSER_VERSION,
            },
            "date": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: TAG_PARSER_DATE,
            },
            "acronym": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: TAG_PARSER_STR,
            },
            "codename": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: TAG_PARSER_STR,
            },
            "doctitle": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: TAG_PARSER_STR,
            },
            "desc": {
                TAG_SPECS_REQUIRED: True,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: TAG_PARSER_STR,
            },
            "author": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: TAG_PARSER_PERSON,
            },
            "authors": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: True,
                TAG_SPECS_PARSER: TAG_PARSER_PERSON,
            },
            "contrib": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: False,
                TAG_SPECS_PARSER: TAG_PARSER_PERSON,
            },
            "contribs": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: True,
                TAG_SPECS_PARSER: TAG_PARSER_PERSON,
            },
            "urls": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
                TAG_SPECS_CONTENT: {
                    TAG_SPECS_ALT_ALL: (),
                    "home": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_POST_PROD: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: TAG_PARSER_URL,
                    },
                    "dev": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_POST_PROD: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: TAG_PARSER_URL,
                    },
                    "issues": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_POST_PROD: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: TAG_PARSER_URL,
                    },
                },
            },
            "licenses": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
                TAG_SPECS_CONTENT: {
                    TAG_SPECS_ALT_ALL: (),
                    "code": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_POST_PROD: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: TAG_PARSER_LICENSE,
                    },
                    "manual": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_POST_PROD: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: TAG_PARSER_LICENSE,
                    },
                },
            },
            "langs": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
                TAG_SPECS_CONTENT: {
                    TAG_SPECS_ALT_ALL: (),
                    "doc": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_POST_PROD: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: TAG_PARSER_LANG,
                    },
                    "manual": {
                        TAG_SPECS_REQUIRED: False,
                        TAG_SPECS_POST_PROD: False,
                        TAG_SPECS_TYPE: TAG_SPECS_DATA,
                        TAG_SPECS_LIST_OF: False,
                        TAG_SPECS_PARSER: TAG_PARSER_LANG,
                    },
                },
            },
            "require": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: True,
                TAG_SPECS_PARSER: TAG_PARSER_STR,
            },
            "keywords": {
                TAG_SPECS_REQUIRED: False,
                TAG_SPECS_POST_PROD: False,
                TAG_SPECS_TYPE: TAG_SPECS_DATA,
                TAG_SPECS_LIST_OF: True,
                TAG_SPECS_PARSER: TAG_PARSER_STR,
            },
        },
    },
    "toc": {
        TAG_SPECS_REQUIRED: False,
        TAG_SPECS_POST_PROD: True,
        TAG_SPECS_TYPE: TAG_SPECS_DATA,
        TAG_SPECS_LIST_OF: True,
        TAG_SPECS_PARSER: TAG_PARSER_TOCPATH,
    },
}
