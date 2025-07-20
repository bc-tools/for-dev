#!/usr/bin/env python3

from dataclasses import dataclass


# ------------------------ #
# -- LICENSE DATA CLASS -- #
# ------------------------ #

###
# Easy-to-use data class for licenses.
###
@dataclass
class License:
    std       : str
    name      : str
    ref       : str
    deprecated: bool

###
# We want to string print the standard code of the license.
###
    def __str__(self) -> str:
        return self.std
