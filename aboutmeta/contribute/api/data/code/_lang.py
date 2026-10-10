#!/usr/bin/env python3

from dataclasses import field

from langcodes import (
    get as get_langcode,
    LanguageTagError
)

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
    name      : str = field(init=False)
    territory : str = field(init=False)

    def __post_init__(self):
        self.name = 0
        self.territory = 1



# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    mydata = Lang(identifier = 'fr')

    print()

    print("Original data")
    print(mydata)

    print()
