#!/usr/bin/env python3

###
# Information related to a person is indicated as follows.
#
#     + **Title (mandatory):** ''Krivine'' and ''Jean, Louis,
#     Krivine'' are legal titles for a person (the number of
#     first names is unlimited). It is possible to specify a
#     particle, as in ''Augustus, {de} Morgan''.
#
#     + **Email address (optional):** ''Jean, Louis, Krivine
#     [jl-krivine@compile.brain]'' adds an email using square
#     brackets.
#
#     + **Affiliation (optional):** ''Torvalds (Sacred Kernels
#     Department)'' adds an affiliation using parentheses.
#
#     + **Indicate everything:** the only format allowed is
#     ''title [email] (institute)'' like in ''Ada, Lovelace
#     [ada.babbage.computer@paper.org] (Victorian Applied
#     Mechanical Informatic Institute)''.
#
#
# [[normalize]]
#
# Here are the normalization steps performed.
#
#     + Names are written in "titlecase", and the particle in
#     lowercase. Spaces around the hyphen are removed.
#     For example,''ALIce,  MarIE   -  LiSe,   {DE}   Charlène''
#     becomes ''Alice, Marie-Lise, {de} Charlène''.
#
#     + Some valid emails adresses use typographical quirks.
#     For example, ''SuPpOrT@OpeAI.CoM'' is valid, but its
#     normalized version is ''SuPpOrT@openai.com''.
#
#     + The normalization of the affiliation address is limited
#     to not having consecutive spaces. For example,
#     ''Université   de   la Technologie,    France'' becomes
#     ''Université de la Technologie, France''.
#
#
# [[validate]]
#
# Here are the validation steps performed.
#
#     + The email syntax is verified.
#
#     + OpenStreetMap is used to verify the existence of the
#     affiliation.
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
#     :return: the \std \yaml version of the ''Person'' object.
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

    yaml_data   = "Alice, Marie-Lise, {Mc} Someone [e.mail@provided.by] (My address)"
    data_parsed = parse(yaml_data)

    print()
    print('~~~')

    print()
    print(f"{yaml_data          = }")
    print(f"{data_parsed        = }")
    print(f"{write(data_parsed) = }")
