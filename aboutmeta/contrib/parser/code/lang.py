#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.data.errors import ParsingError

from aboutmeta.data import lang

from langcodes import (
    get as get_langcode,
    LanguageTagError
)


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     data : the \lang provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''lang.Lang'' to work easily
#              with the \lang.
###
def parse(data: str) -> lang.Lang:
# Getting a normalized code.
    try:
        onelang = get_langcode(data).maximize()

    except LanguageTagError as e:
        message = str(e)
        message = message[0].lower() + message[1:]

        raise ParsingError(message)

# Small description of the language code.
    describe = onelang.describe('en')

# Patch for the strange "Unknow language".
    if describe['language'].startswith('Unknown language'):
        raise ParsingError(f"unknown language code '{data}'")

# The job has been done.
    return lang.Lang(
        std       = f"{onelang.language}-{onelang.territory}",
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

        onelang = parse(userlang)

        print(onelang)
        print(repr(onelang))

    print()

# Corrupted data.
    userlang = "XXXXXXXX"
    # userlang = "XXX"

    print(f'--- ({userlang}) --> CORRUPTED!')

    onelang = parse(userlang)
