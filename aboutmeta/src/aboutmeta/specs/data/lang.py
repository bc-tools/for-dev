#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/data/code/lang.py'


from langcodes import (
    get as get_langcode,
    LanguageTagError
)


from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ---------- #
# -- DATA -- #
# ---------- #

###
# prototype::
#     std_id    : the standard language identifier which looks
#                 like ''en-GB''.
#     name      : the full language name like ''English''.
#     territory : the territory of the language like ''Great
#                 Britain''.
#
#
# note::
#     The ''name'' and ''territory'' attributes are build from
#     the value of the ''std_id'' attribute.
#
#
# warning::
#     Short identifiers are automatically expanded to full ones
#     regardless of letter casing: if a user enters ''fr'' or
#     ''FR-fr'', it will be saved as ''fr-FR''. Enforcing this
#     normalization \std at the \yaml input stage is a best
#     practice.
###
class Lang(DataManager):
    std_id   : str
    name     : str = field(init = False)
    territory: str = field(init = False)

###
# prototype::
#     :action: derive the ''name'' and ''territory'' attributes
#     from ''self.std_id'' and expand the identifier to its full
#     form (e.g., ''fr'' becomes ''fr-FR'').
###
    def __post_init__(self) -> None:
# Getting a normalized code.
        try:
            lang = get_langcode(self.std_id).maximize()

        except LanguageTagError as e:
            msg = str(e)
            msg = msg[0].lower() + msg[1:]

            raise ParsingError(msg)

# Small description of the language code.
        desc = lang.describe('en')

# Patch for the strange "Unknow language".
        if desc['language'].startswith('Unknown language'):
            raise ValueError(
                f"unknown language code '{self.std_id}'"
            )

# The job has been done.
        self.std_id    = f"{lang.language}-{lang.territory}"
        self.name      = desc["language"]
        self.territory = desc["territory"]
