#!/usr/bin/env python3

from dataclasses import dataclass


# ------------------------- #
# -- LANGUAGE DATA CLASS -- #
# ------------------------- #

### TODO
# prototype::
#     std       : the standard version of the yaml version
#     name      : str
#     territory :
###
@dataclass(frozen = True)
class Lang(DataPrinter):
    std      : str
    name     : str
    territory: str
