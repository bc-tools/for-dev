#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #

from aboutmeta.specs.constants import *


# --------------- #
# -- ALL SPECS -- #
# --------------- #

SPECS = {
    TAG_FLAVOUR_IT_PROJECT: {
        TAG_SPECS_OPTIONAL: {"toc", "project"},
        TAG_SPECS_REQUIRED: set(),
    },
    TAG_FLAVOUR_TOC: {TAG_SPECS_OPTIONAL: set(), TAG_SPECS_REQUIRED: {"toc"}},
}
