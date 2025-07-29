#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.data.errors import ParsingError

from aboutmeta.data import url


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     data : one \url provided in the \yaml file, but stripped.
#
#     :return: an exact copy of the data.
#
#
# note::
#     This fake parser greatly simplifies the part that handles
#     online validations.
###
def parser(data: str) -> url.URL:
# We do almost nothing...
    return url.URL(url = data)
