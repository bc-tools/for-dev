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
            TAG_KEY_AUTHOR,
            TAG_KEY_AUTHORS,
            TAG_KEY_CODENAME,
            TAG_KEY_CONTRIB,
            TAG_KEY_CONTRIBS,
            TAG_KEY_DOCTITLE,
        ),
        TAG_SPECS_ALT_TUPLES: (
            (TAG_KEY_AUTHOR, TAG_KEY_AUTHORS),
            (TAG_KEY_CODENAME, TAG_KEY_DOCTITLE),
            (TAG_KEY_CONTRIB, TAG_KEY_CONTRIBS),
        ),
        TAG_KEY_VERSION: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: sem_version_parse,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_DATE: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: date_parse,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_ACRONYM: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_CODENAME: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_DOCTITLE: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_DESC: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: True,
        },
        TAG_KEY_AUTHOR: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_AUTHORS: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_CONTRIB: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: False,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_CONTRIBS: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: person_parse,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_URLS: {
            TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
            TAG_SPECS_CONTENT: {
                TAG_SPECS_ALT_ALL: None,
                TAG_KEY_HOME: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: url_parse,
                    TAG_SPECS_MAPPER: None,
                    TAG_SPECS_REQUIRED: False,
                },
                TAG_KEY_DEV: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: url_parse,
                    TAG_SPECS_MAPPER: None,
                    TAG_SPECS_REQUIRED: False,
                },
                TAG_KEY_ISSUES: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: url_parse,
                    TAG_SPECS_MAPPER: None,
                    TAG_SPECS_REQUIRED: False,
                },
            },
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_LICENSES: {
            TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
            TAG_SPECS_CONTENT: {
                TAG_SPECS_ALT_ALL: None,
                TAG_KEY_CODE: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: license_parse,
                    TAG_SPECS_MAPPER: None,
                    TAG_SPECS_REQUIRED: False,
                },
                TAG_KEY_MANUAL: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: license_parse,
                    TAG_SPECS_MAPPER: None,
                    TAG_SPECS_REQUIRED: False,
                },
            },
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_LANGS: {
            TAG_SPECS_TYPE: TAG_SPECS_BLOCK,
            TAG_SPECS_CONTENT: {
                TAG_SPECS_ALT_ALL: None,
                TAG_KEY_DOC: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: lang_parse,
                    TAG_SPECS_MAPPER: None,
                    TAG_SPECS_REQUIRED: False,
                },
                TAG_KEY_MANUAL: {
                    TAG_SPECS_TYPE: TAG_SPECS_DATA,
                    TAG_SPECS_LIST_OF: False,
                    TAG_SPECS_PARSER: lang_parse,
                    TAG_SPECS_MAPPER: None,
                    TAG_SPECS_REQUIRED: False,
                },
            },
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_REQUIRE: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: False,
        },
        TAG_KEY_KEYWORDS: {
            TAG_SPECS_TYPE: TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF: True,
            TAG_SPECS_PARSER: None,
            TAG_SPECS_MAPPER: None,
            TAG_SPECS_REQUIRED: False,
        },
    },
}
