#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.data import constants, person
from aboutmeta.tool import group


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : one person provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''person.Person'' to work
#              easily with the person data.
###
def parser(content: str) -> person.Person: # abc  #def
# One affiliation?
    content, affiliation = group.extract_group(
        content = content,
        opener  = constants.TAG_YAML_AFFILIATION_OPEN,
        closer  = constants.TAG_YAML_AFFILIATION_CLOSE,
        context = "affiliation"
    )

# One email?
    content, email = group.extract_group(
        content = content,
        opener  = constants.TAG_YAML_EMAIL_OPEN,
        closer  = constants.TAG_YAML_EMAIL_CLOSE,
        context = "email"
    )

# Titles of the person.
    titles = content.split(',')

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
        print()
        print(f'---\n{someone}\n---')

        someone_data = parser(someone)

        print(repr(someone_data))

        print(someone_data)

        print()

# Corrupted data.
    someone = "ABC)"
    someone = "AB(C"
    someone = "AB](C)"
    someone = "A[B(C)"

    print(f'---\n{someone} --> CORRUPTED!\n---')

    someone_data = parser(someone)
