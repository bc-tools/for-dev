#!/usr/bin/env python3

from dataclasses import dataclass

from aboutmeta.core.dataprinter import *


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
###
@dataclass(frozen = True)
class Lang(DataPrinter):
    std      : str
    name     : str
    territory: str
