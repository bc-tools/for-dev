#!/usr/bin/env python3

from langcodes import (
    get as get_langcode,
    LanguageTagError
)

from aboutmeta.core.errors     import ParsingError
from aboutmeta.specs.data.lang import Lang


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : the \lang provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''Lang''.
###
def parse(data: str) -> Lang:
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
        raise ValueError(f"unknown language code '{data}'")

# The job has been done.
    return Lang(
        identifier = f"{onelang.language}-{onelang.territory}",
        name       = describe["language"],
        territory  = describe["territory"]
    )


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''Lang'' object.
#
#     :return: the standard \yaml version of the ''Lang'' object
#              which is the full language identifier.
###
def write(data: Lang) -> str:
    return data.identifier


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print()
    print("-- GOOD CASES --")

    for str_data in [
        "fr",
        "es",
        "en",
        "en-GB",
    ]:
        data_parsed = parse(str_data)

        print()
        print('~~~')

        print()
        print(f"{str_data = }")

        print()
        print(repr(data_parsed))

        std_yaml_data = write(data_parsed)

        print()
        print(f"{std_yaml_data = }")


# BAD
    # exit()

    print()
    print("-- BAD CASES --")

    for str_data in [
        "X - X - X",
        "XXX",
    ]:
        print()
        print(f"{str_data = }")

        try:
            parse(str_data)

        except Exception as e:
            print(type(e).__name__, ':', e)
