#!/usr/bin/env python3

from dataclasses import field

from langcodes import (
    get as get_langcode,
    LanguageTagError
)

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ------------------ #
# -- DATA MANAGER -- #
# ------------------ #

###
# prototype::
#     identifier : the standard language identifier which looks
#                  like ''en-GB''.
#     name       : the full language name like ''English''.
#     territory  : the territory of the language like ''Great
#                  Britain''.
#
#
# note::
#     The ''name'' and ''territory'' attributes are build from
#     the value of the ''identifier'' attribute.
#
#
# warning::
#     Short identifiers are automatically expanded to full ones.
#     If a user enters ''fr'', it will be saved as ''fr-FR''.
#     Enforcing this normalization standard at the \yaml input stage
#     is a recommended best practice.
###
class Lang(DataManager):
    identifier: str
    name      : str = field(init = False)
    territory : str = field(init = False)

###
# prototype::
#     :action: derive the ''name'' and ''territory'' attributes
#     from ''self.identifier'' and expand the identifier to its
#     full form (e.g., ''fr'' becomes ''fr-FR'').
###
    def __post_init__(self):
# Getting a normalized code.
        try:
            lang = get_langcode(self.identifier).maximize()

        except LanguageTagError as e:
            msg = str(e)
            msg = msg[0].lower() + msg[1:]

            raise ParsingError(msg)

# Small description of the language code.
        desc = lang.describe('en')

# Patch for the strange "Unknow language".
        if desc['language'].startswith('Unknown language'):
            raise ValueError(f"unknown language code '{self.identifier}'")

# The job has been done.
        self.identifier = f"{lang.language}-{lang.territory}"
        self.name       = desc["language"]
        self.territory  = desc["territory"]


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from aboutmeta.core.log_conf import *
    setup_logging()

# GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    for identifier in [
        "fr",
        "es",
        "en",
        "en-GB",
    ]:
        mydata = Lang(identifier = identifier)

        print()
        print(f"{identifier = }")
        print(f"{mydata     = }")


# BAD
    # exit()

    print("\n------------\n")

    print("-- BAD CASES --")

    for identifier in [
        "X - X - X",
        "XXX",
    ]:
        print()
        print(f"{identifier = }")

        try:
            Lang(identifier = identifier)

        except Exception as e:
            print(type(e).__name__, ':', e)
