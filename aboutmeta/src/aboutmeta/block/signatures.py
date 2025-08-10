#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #

from aboutmeta.block.constants import *


# ---------------- #
# -- SIGNATURES -- #
# ---------------- #

SIGNATURES = {
    "date_parse": [CTXT_DATA],
    "lang_parse": [CTXT_DATA],
    "license_parse": [CTXT_DATA],
    "person_parse": [CTXT_DATA],
    "sem_version_parse": [CTXT_DATA],
    "url_parse": [CTXT_DATA],
    "virtual_path_parse": [TAG_ARG_PARENT, CTXT_DATA],
    "virtual_path_map": [TAG_ARG_AMDATA_CLS, TAG_ARG_DATA_LIST],
}
