#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #

from aboutmeta.specs.constants import *


# ---------------- #
# -- SIGNATURES -- #
# ---------------- #

SPECS = {
    "date_parse": [TAG_ARG_DATA],
    "lang_parse": [TAG_ARG_DATA],
    "license_parse": [TAG_ARG_DATA],
    "person_parse": [TAG_ARG_DATA],
    "sem_version_parse": [TAG_ARG_DATA],
    "url_parse": [TAG_ARG_DATA],
    "virtual_path_parse": [TAG_ARG_PARENT, TAG_ARG_DATA],
    "virtual_path_map": [TAG_ARG_AMDATA_CLS, TAG_ARG_DATA_LIST],
}
