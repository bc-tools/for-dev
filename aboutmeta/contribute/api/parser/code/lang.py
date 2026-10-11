#!/usr/bin/env python3

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
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.lang.Lang''.
    return Lang(identifier = data)


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
# We just need some basic interface tests, because we have already
# tested the ''Lang'' class.

# GOOD
    print()
    print("-- GOOD CASES --")

    std_yaml_data = "fr"
    data_parsed   = parse(std_yaml_data)

    print()
    print('~~~')

    print()
    print(f"{std_yaml_data = }")

    print()
    print(repr(data_parsed))

    std_yaml_data = write(data_parsed)

    print()
    print(f"{std_yaml_data = }")
