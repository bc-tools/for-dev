#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #

from aboutmeta.specs.constants import *


# --------------- #
# -- EASY TAGS -- #
# --------------- #

TAG_FLAVOUR_IT_PROJECT = "it-project"
TAG_FLAVOUR_TOC = "toc"


# --------------- #
# -- ALL SPECS -- #
# --------------- #

SPECS = {
    TAG_FLAVOUR_IT_PROJECT: {
        TAG_SPECS_OPTIONAL: {TAG_FLAVOUR_TOC, "project"},
        TAG_SPECS_REQUIRED: set(),
    },
    TAG_FLAVOUR_TOC: {TAG_SPECS_OPTIONAL: set(), TAG_SPECS_REQUIRED: {TAG_FLAVOUR_TOC}},
}
