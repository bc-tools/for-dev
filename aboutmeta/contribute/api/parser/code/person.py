#!/usr/bin/env python3

###
# Information related to a person is indicated as follows.
#
#     + **Title (mandatory):** ''Krivine'' and ''Jean, Louis,
#       Krivine'' are legal titles for a person (the number
#       of first names is unlimited). It is possible to specify
#       a partcile, as in ''Augustus, {de} Morgan''.
#
#     + **Email address (optional):** ''Jean, Louis, Krivine
#       [jl-krivine@compile.brain]'' adds an email using square
#       brackets.
#
#     + **Affiliation (optional):** ''Torvalds (Sacred Kernels
#       Department)'' adds an affiliation using parentheses.
#
#     + **Indicate everything:** the only format allowed is
#       ''<title> [email] (institute)'' like in ''Ada, Lovelace
#       [ada.babbage.computer@paper.org] (Victorian Applied
#       Mechanical Informatic Institute)''.
#
#
# [[normalize]]
# ...
#
#
# [[validate]]
# ...
###


from aboutmeta.specs.data.person import Person


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : one person provided in the \yaml file, but stripped.
#
#     :return: an instance of the ''Person'' class.
###
def parse(data: str) -> Person:
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.person.Person''.
    return Person(spec = data)


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''Person'' object.
#
#     :return: the standard \yaml version of the ''Person'' object.
###
def write(data: Person) -> str:
    return data.spec


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# We just need some basic interface tests, because we have already
# tested the ''Person'' class.

# GOOD
    print()
    print("-- GOOD CASES --")

    std_yaml_data = "Alice, Marie-Lise, {Mc} Someone [e.mail@provided.by] (My address)"
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
