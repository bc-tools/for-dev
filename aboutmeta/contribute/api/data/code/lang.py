#!/usr/bin/env python3

from langcodes import (
    get as get_langcode,
    LanguageTagError
)


from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError
from aboutmeta.core.validate     import validate_type


# ---------- #
# -- DATA -- #
# ---------- #

###
# prototype::
#     std_id    : the \std \lang identifier like ''"en-GB"''.
#     name      : the full \lang name like ''"English"''.
#     territory : the territory of the \lang like ''"Great
#                 Britain"''.
#
#
# note::
#     The ''name'' and ''territory'' \attrs are build from the
#     \val of the ''std_id'' \attr.
#
#
# warning::
#     Short identifiers are automatically expanded to full ones
#     regardless of letter casing: ''"fr"'' and ''"FR-fr"'' are
#     saved as ''"fr-FR"''.
#     Enforcing this normalization \std at the \yaml input stage
#     is a painless best practice.
###
class Lang(DataManager):
    std_id   : str
    name     : str = field(init = False)
    territory: str = field(init = False)

###
# prototype::
#     :action: mandatory validations of ''self.std_id'' type, and
#              derivation of the ''name'' and ''territory'' \attrs
#              from ''self.std_id'' and expand the identifier to
#              its full form (e.g., ''"fr"'' becomes ''"fr-FR"'').
###
    def __post_init__(self) -> None:
        validate_type(
            data_name      = 'std_id',
            data           = self.std_id,
            types_expected = str,
        )

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


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print('')
    print("-- GOOD CASES --")

    for yaml_data in [
        "fr",
        "es",
        "en",
        "en-GB",
        "eN-gb",
        "eN_gb",
    ]:
        mydata = Lang(std_id = yaml_data)

        print()
        print(f"{yaml_data = }")
        print(f"{mydata    = }")

# BAD
    # exit()

    print('')
    print("-- BAD CASES --")

    for yaml_data in [
        123,
        "X - X - X",
        "XXX",
    ]:
        print()
        print(f"{yaml_data = }")

        try:
            Lang(std_id = yaml_data)

        except Exception as e:
            print(type(e).__name__, ':', e)
