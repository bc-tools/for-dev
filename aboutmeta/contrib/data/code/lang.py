#!/usr/bin/env python3

from dataclasses import dataclass

from aboutmeta.core.dataprinter import DataPrinter


# ------------------------- #
# -- TOOLS -- #
# ------------------------- #

# ------------------------- #
# -- LANGUAGE DATA CLASS -- #
# ------------------------- #

###
# prototype::
#     std       : the standard language identifier which looks
#                 like ''en-GB''.
#     name      : the full language name like ''English''.
#     territory : the territory of the language like ''Great
#                 Britain''.
#
#
# note::
#     The ''std'' attribute is part of the frozen dataclass
#     ''DataPrinter''.
###
@dataclass(frozen = True)
class Lang(DataPrinter):
    name     : str
    territory: str
