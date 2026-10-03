#!/usr/bin/env python3

from aboutmeta.core.data_manager import DataManager


# ------------------- #
# -- MY DATA CLASS -- #
# ------------------- #

###
# prototype::  A REVOIR
#     XXX : YYYY
#
#
# "[about] [meta]data" stored as
#     + short = "aboutmeta"
#     + full  = "about metadata"
#     + parts = [
#         ("about", True ),  # keep = True
#         (" "    , False),  # keep = False
#         ("meta" , True ),  # keep = True
#         ("data" , False),  # keep = False
#     ]
###
class Acronym(DataManager):
    yaml_val: str


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Nothing to test!
    ...
