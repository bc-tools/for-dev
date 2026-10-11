#!/usr/bin/env python3

from aboutmeta.specs.data.acronym import Acronym


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : the acronym provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''Acronym''.
###
def parse(data: str) -> Acronym:
    ...


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''Acronym'' object.
#
#     :return: the standard \yaml version of the ''Acronym'' object.
###
def write(data: Acronym) -> str:
    ...


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    ...
