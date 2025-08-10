#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #

from aboutmeta.specs.constants import *


# ----------- #
# -- SPECS -- #
# ----------- #

SPECS = {
    TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
    TAG_SPECS_CONTENT: {
        TAG_SPECS_ALT_ALL: (
            TAG_KEY_author,
            TAG_KEY_authors,
            TAG_KEY_codename,
            TAG_KEY_contrib,
            TAG_KEY_contribs,
            TAG_KEY_doctitle,
        ),
        TAG_SPECS_ALT_TUPLES: (
            (TAG_KEY_author, TAG_KEY_authors),
            (TAG_KEY_codename, TAG_KEY_doctitle),
            (TAG_KEY_contrib, TAG_KEY_contribs),
        ),
        TAG_KEY_version: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: sem_version_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_date: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: date_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_acronym: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_codename: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_doctitle: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_desc: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: True,
        },
        TAG_KEY_author: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_authors: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_contrib: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_contribs: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_urls: {
            TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
            TAG_SPECS_CONTENT: {
                TAG_SPECS_ALT_ALL: None,
                TAG_KEY_home: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: url_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
                TAG_KEY_dev: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: url_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
                TAG_KEY_issues: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: url_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
            },
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_licenses: {
            TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
            TAG_SPECS_CONTENT: {
                TAG_SPECS_ALT_ALL: None,
                TAG_KEY_code: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: license_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
                TAG_KEY_manual: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: license_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
            },
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_langs: {
            TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
            TAG_SPECS_CONTENT: {
                TAG_SPECS_ALT_ALL: None,
                TAG_KEY_doc: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: lang_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
                TAG_KEY_manual: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: lang_parse,
                    TAG_SPECS_POST_PROD: False,
                    TAG_SPECS_REQUIRED: False,
                },
            },
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_require: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_keywords: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_POST_PROD: False,
            TAG_SPECS_REQUIRED: False,
        },
    },
}
