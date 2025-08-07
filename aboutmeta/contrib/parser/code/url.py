#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.data.url import URL


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : one \url provided in the \yaml file, but stripped.
#
#     :return: an exact copy of the data.
#
#
# note::
#     The sole purpose of this fake parser is to generate an
#     internal ''URL'' class that can be used to validate
#     and normalize a URL.
###
def parse(data: str) -> URL:
# We do almost nothing... But what we do is great!
    return URL(std = data)
