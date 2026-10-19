#!/usr/bin/env python3

###
# The origin of an acronym can be explained using a tiny DSL.
# For example, ''"[A::@-]bout [Desc]ription"'' explains the
# choice of the acronym '@-Desc' for 'About Description'.
# Here is how it works.
#
#     1) First, we have the full name "About Description".
#
#     1) Then, we indicate inside brackets the parts to keep
#     for the acronym. Using "[A]bout [Desc]ription" will
#     produce the acronym "Adesc".
#
#     1) To change a part of the acronym, we use ''::'', as in
#     ''"[A::@-]bout [Desc]ription"'', to indicate "@-" instead
#     of "A".
###


from aboutmeta.specs.data.acronym import Acronym


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : the acronym provided in the \yaml file, but
#            stripped.
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
#     :return: the standard \yaml version of the ''Acronym''
#              object.
###
def yamlify(data: Acronym) -> str:
    return data.spec


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# We just need some basic interface tests, because we have
# already tested the ''Acronym'' class.

# GOOD
    print()
    print("-- GOOD CASES --")

    yaml_data   = "[about::@] [meta]data"
    data_parsed = parse(yaml_data)

    print()
    print('~~~')

    print()
    print(f"{yaml_data            = }")
    print(f"{data_parsed          = }")
    print(f"{yamlify(data_parsed) = }")
