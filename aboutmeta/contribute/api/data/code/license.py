#!/usr/bin/env python3

from pathlib import Path

from aboutmeta.core.data_manager import DataManager
from aboutmeta.tool.web          import get_text_from





# ------------------------ #
# -- LICENSE DATA CLASS -- #
# ------------------------ #

###
# prototype::
#     identifier : the short SPDX identifier, such as ''GPL-3.0-only''.
#     name       : the full license name like ''GNU General Public
#                  License v3.0 only''.
#     url        : the URL linking to the SPDX online description of
#                  the license.
###
class License(DataManager):
    identifier: str
    name      : str
    url       : str


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Nothing to test!
    ...
