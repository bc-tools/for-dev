#!/usr/bin/env python3

from aboutmeta.core.data_manager import DataManager


# ------------------------- #
# -- LANGUAGE DATA CLASS -- #
# ------------------------- #

###
# prototype::
#     identifier : the standard language identifier which looks
#                  like ''en-GB''.
#     name       : the full language name like ''English''.
#     territory  : the territory of the language like ''Great
#                  Britain''.
###
class Lang(DataManager):
    identifier: str
    name      : str
    territory : str


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Nothing to test!
    ...
