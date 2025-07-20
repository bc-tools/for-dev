#!/usr/bin/env python3

from dataclasses import dataclass


# ------------------------- #
# -- LANGUAGE DATA CLASS -- #
# ------------------------- #

###
# Easy-to-use data class for languages.
###
@dataclass
class Lang:
    std      : str
    name     : str
    territory: str

###
# We want to string print the standard code of the language.
###
    def __str__(self) -> str:
        return self.std
