#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.data.errors import ParsingError

from aboutmeta.data import constants, person
from aboutmeta.tool import group


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     data : one person provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''person.Person'' to work
#              easily with the person data.
###
def parse(data: str) -> person.Person:
# One affiliation?
    data, affiliation = group.extract_group(
        content = data,
        opener  = constants.TAG_YAML_AFFILIATION_OPEN,
        closer  = constants.TAG_YAML_AFFILIATION_CLOSE,
        context = "affiliation"
    )

# One email?
    data, email = group.extract_group(
        content = data,
        opener  = constants.TAG_YAML_EMAIL_OPEN,
        closer  = constants.TAG_YAML_EMAIL_CLOSE,
        context = "email"
    )

# Affiliation before email?
    if (
        not email is None
        and
        data[-1] == constants.TAG_YAML_AFFILIATION_CLOSE
    ):
        raise ParsingError("affiliation must be after email!")

# Titles of the person.
    titles = data.split(',')

    if len(titles) == 1:
        firstnames = None

    else:
        firstnames = [
            n.strip() for n in titles[:-1]
        ]

    surname = titles[-1].lstrip()

# The job has been done.
    return person.Person(
        firstnames  = firstnames,
        surname     = surname,
        email       = email,
        affiliation = affiliation
    )


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
# Working examples.
    for someone in [
        "A,B,C[a.b.c@d.e](fgh)",
        "A  ,  B   , C   [  a.b.c@d.e  ]  (  fgh  )",
        "A,B,C[a.b.c@d.e]",
        "A,B,C(fgh)",
        "A,B,C",
        "A,B",
        "A",
    ]:
        print(f'---\nPERSON: {someone}')

        someone_data = parse(someone)

        print(repr(someone_data))

        print(someone_data)

# Corrupted data.
    someone = "ABC)"
    someone = "AB(C"
    someone = "AB](C)"
    someone = "A[B(C)"
    # someone = "A(B)[C]"

    print(f'---\nPERSON: {someone} --> CORRUPTED!\n---')

    someone_data = parse(someone)
