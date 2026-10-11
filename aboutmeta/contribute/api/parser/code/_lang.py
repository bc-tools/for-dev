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
    TODO


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
    ...
