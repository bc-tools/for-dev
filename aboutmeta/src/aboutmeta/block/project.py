#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #

from aboutmeta.block.constants import *


# ----------- #
# -- SPECS -- #
# ----------- #

SPECS = {
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
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: sem_version_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        "date": {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: date_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        "acronym": {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        "codename": {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        "doctitle": {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        "desc": {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: True,
        },
        "author": {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        "authors": {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        "contrib": {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        "contribs": {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        "urls": {
            TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
            TAG_SPECS_CONTENT: {
                TAG_SPECS_ALT_ALL: None,
                "home": {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: url_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
                "dev": {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: url_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
                "issues": {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: url_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
            },
            TAG_SPECS_REQUIRED: False,
        },
        "licenses": {
            TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
            TAG_SPECS_CONTENT: {
                TAG_SPECS_ALT_ALL: None,
                "code": {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: license_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
                "manual": {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: license_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
            },
            TAG_SPECS_REQUIRED: False,
        },
        "langs": {
            TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
            TAG_SPECS_CONTENT: {
                TAG_SPECS_ALT_ALL: None,
                "doc": {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: lang_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
                "manual": {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: lang_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
            },
            TAG_SPECS_REQUIRED: False,
        },
        "require": {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        "keywords": {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
    },
}
