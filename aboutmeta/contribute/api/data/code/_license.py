#!/usr/bin/env python3

from dataclasses import field

from json import (
    dumps as json_dumps,
    load  as json_load,
)

from pathlib import Path
import              re

from rapidfuzz import (
    process as fuzz_process,
    fuzz
)

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.constants    import *
from aboutmeta.core.errors       import ParsingError
from aboutmeta.tool.web          import get_text_from


# ------------------ #
# -- DATA MANAGER -- #
# ------------------ #

LICENSES_JSON_FILE = Path(__file__).parent / "license-spdx.json"


###
# prototype::
#     identifier : the short SPDX identifier, such as ''GPL-3.0-only''.
#     name       : the full license name like ''GNU General Public
#                  License v3.0 only''.
#     url        : the URL linking to the SPDX online description of
#                  the license.
#
#
# note::
#     The ''name'' and ''url'' attributes are build from the value of the ''identifier'' attribute.
#
#
# warning::
#     Identifiers are automatically normalized regardless of letter casing: if a user enters '???', it will be saved as '???'. Enforcing this normalization standard at the \yaml input stage is a best practice.
###
class License(DataManager):
    identifier: str
    name      : str = field(init = False)
    url       : str = field(init = False)

###
# prototype::
#     :action: derive the ''name'' and ''url'' attributes from ''self.identifier'' and expand the identifier to its normalized form (e.g., ''???'' becomes ''???'').
###
    def __post_init__(self):
        ...


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Nothing to test!
    ...
