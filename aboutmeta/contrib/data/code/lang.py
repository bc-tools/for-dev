#!/usr/bin/env python3

from dataclasses import dataclass

from aboutmeta.core.dataprinter import *


# ------------------------- #
# -- LANGUAGE DATA CLASS -- #
# ------------------------- #

###
# prototype::
#     std       : the standard language identifier, such as ''en-GB''.
#     name      : the full language name.
#     territory : the territory of the language.
###
@dataclass(frozen = True)
class Lang(DataPrinter):
    std      : str
    name     : str
    territory: str
