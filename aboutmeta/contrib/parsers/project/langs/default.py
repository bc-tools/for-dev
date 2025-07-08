#!/usr/bin/env python3

import aboutmeta


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

from langcodes import (
    get as getlangcode,
    LanguageTagError
)

###
# prototype::
#     content :
#
#     :return:
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


# ----------------------------- #
# -- HUMAN TESTS (MANDATORY) -- #
# ----------------------------- #

if __name__ == "__main__":
    for userlang in [
        "fr",
        "es",
        "en-GB",
        # "XXXXXX"   # BUG!
    ]:
        print()
        print(f'--- ({userlang})')

        lang = parser(userlang)

        print(lang)
        print(repr(lang))

    print()
