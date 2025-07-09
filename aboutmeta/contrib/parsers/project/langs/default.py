#!/usr/bin/env python3

import aboutmeta


# ------------- #
# -- IMPORTS -- #
# ------------- #

from langcodes import (
    get as getlangcode,
    LanguageTagError
)


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

### TODO
# prototype::
#     content : XXX
#
#     :return: XXX
###
def parser(content: str) -> aboutmeta.data.lang.Lang:
# Getting a normalized code.
    try:
        lang = getlangcode(content).maximize()

    except LanguageTagError as e:
        raise ValueError(f"illegal language code ''{content}''")

# Small description of the language code.
    describe = lang.describe('en')

# The job has been done.
    return aboutmeta.data.lang.Lang(
        std       = f"{lang.language}-{lang.territory}",
        name      = describe["language"],
        territory = describe["territory"]
    )


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
    for userlang in [
        "fr",
        "es",
        "en-GB",
        # "XXXXXX"   # Test of an exception.
    ]:
        print()
        print(f'--- ({userlang})')

        lang = parser(userlang)

        print(lang)
        print(repr(lang))

    print()
