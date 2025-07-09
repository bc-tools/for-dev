#!/usr/bin/env python3

import aboutmeta


# ------------- #
# -- IMPORTS -- #
# ------------- #

from langcodes import (
    get as get_langcode,
    LanguageTagError
)


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : the \lang provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''aboutmeta.data.lang.Lang''
#              to work easily with the \lang.
###
def parser(content: str) -> aboutmeta.data.lang.Lang:
# Getting a normalized code.
    try:
        lang = get_langcode(content).maximize()

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
# Working examples.
    for userlang in [
        "fr",
        "es",
        "en",
        "en-GB",
    ]:
        print()
        print(f'--- ({userlang})')

        lang = parser(userlang)

        print(lang)
        print(repr(lang))

    print()

# Corrupted data.
    userlang =  "XXXXXX"   # Test of an exception.

    print(f'--- ({userlang}) --> CORRUPTED!')

    lang = parser(userlang)
