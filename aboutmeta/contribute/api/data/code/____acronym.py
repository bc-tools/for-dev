#!/usr/bin/env python3

from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ------------------ #
# -- DATA MANAGER -- #
# ------------------ #

###
# prototype::  A REVOIR
#     XXX : YYYY
#
#
# "[about] [meta]data" stored as
#     + short = "aboutmeta"
#     + desc  = "about metadata"
#     + parts = (
#         ("about", "about"),
#         (" "    , None),
#         ("meta" , "meta"),
#         ("data" , None),
#     )
#     + dsl = "[about] [meta]data"
#
#
# "[about=@]    [meta=met@]data" stored as
#     + short = "@met@"
#     + desc  = "about metadata, with '@' for 'about' and 'meta' for 'met@'"
#     + parts = (
#         ("about", "@" ),
#         (" "    , None),
#         ("meta" , "met@"),
#         ("data" , None),
#     )
#     + dsl = "[about=@] [meta=met@]data"
###
class Acronym(DataManager):
    short: str
    desc : str                     = field(init = False)
    parts: tuple(tuple(str, bool)) = field(init = False)
    dsl  : str                     = field(init = False)

###
# prototype::  XXXX
#     :action: derive the ''name'' and ''territory'' attributes
#     from ''self.identifier'' and expand the identifier to its
#     full form (e.g., ''fr'' becomes ''fr-FR'').
###
    def __post_init__(self):
        ...


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Nothing to test!
    ...
