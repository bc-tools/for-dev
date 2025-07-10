#!/usr/bin/env python3

import aboutmeta


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : one person provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''aboutmeta.data.person.Person''
#              to work easily with the person data.
###
def parser(content: str) -> aboutmeta.data.person.Person:
# One affiliation?
    content, affiliation = aboutmeta.tools.group.extract_group(
        content = content,
        opener  = aboutmeta.data.constants.TAG_AFFILIATION_OPEN,
        closer  = aboutmeta.data.constants.TAG_AFFILIATION_CLOSE,
        context = "affiliation"
    )

# One email?
    content, email = aboutmeta.tools.group.extract_group(
        content = content,
        opener  = aboutmeta.data.constants.TAG_EMAIL_OPEN,
        closer  = aboutmeta.data.constants.TAG_EMAIL_CLOSE,
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
    return aboutmeta.data.person.Person(
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

        s = parser(someone)

        print(repr(s))

        print(s)

        print()

# Corrupted data.
    someone = "ABC)"
    someone = "AB(C"
    someone = "AB](C)"
    someone = "A[B(C)"

    print(f'---\n{someone} --> CORRUPTED!\n---')

    s = parser(someone)
