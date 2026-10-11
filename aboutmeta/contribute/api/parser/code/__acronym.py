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
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.acronym.Acronym''.
    return Acronym(spec = data)


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
    return data.acro


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    ...
