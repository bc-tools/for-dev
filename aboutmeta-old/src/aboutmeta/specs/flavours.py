#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #

from aboutmeta.specs.block.project import SPECS as project_specs
from aboutmeta.specs.block.toc import SPECS as toc_specs


# --------------- #
# -- ALL SPECS -- #
# --------------- #

SPECS = {
    TAG_FLAVOUR_IT_PROJECT: {
        TAG_SPECS_OPTIONAL: [TAG_KEY_PROJECT, TAG_KEY_TOC],
        TAG_SPECS_REQUIRED: [],
        TAG_SPECS_TOOLS: {TAG_KEY_PROJECT: project_specs, TAG_KEY_TOC: toc_specs},
    },
    TAG_FLAVOUR_TOC: {
        TAG_SPECS_OPTIONAL: [],
        TAG_SPECS_REQUIRED: [TAG_KEY_TOC],
        TAG_SPECS_TOOLS: {TAG_KEY_TOC: toc_specs},
    },
}
