#!/usr/bin/env python3

from aboutmeta.core.constants    import *
from aboutmeta.core.errors       import ParsingError
from aboutmeta.specs.data.person import Person
from aboutmeta.tools.group       import extract_group


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : one person provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''Person'' to work easily
#              with the person data.
###
def parse(data: str) -> Person:
# One affiliation?
    data, affiliation = extract_group(
        content = data,
        delims  = DELIMS_AFFILIATION,
        context = "affiliation"
    )

# One email?
    data, email = extract_group(
        content = data,
        delims  = DELIMS_EMAIL,
        context = "email"
    )

# First names.
    titles = data.split(',')

    if len(titles) == 1:
        firstnames = []

    else:
        firstnames = [n.strip() for n in titles[:-1]]

# Surname.
    main_name, particle = extract_group(
        content      = titles[-1].strip(),
        delims       = DELIMS_PARTICLE,
        context      = "surname",
        data_on_left = False
    )

# The job has been done.
    return Person(
        surname     = main_name,
        particle    = particle,
        firstnames  = firstnames,
        email       = email,
        affiliation = affiliation,
    )


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    for str_data in [
        "Someone",
        "ALIce, MarIE-LiSe, Someone (My address)",
        "Someone [e.mail@provided.by]",
        "Someone [e.mail@provided.by] (My address)",
        "ALIce,    MarIE-LiSe,   {DE}    Someone   [   e.mail@provided.by ]    (   My   address  )",
    ]:
        print()

        data_parsed = parse(str_data)

        print(f"{str_data = }")
        print(repr(data_parsed))

# BAD
    # exit()

    print("\n------------\n")

    print("-- BAD CASES --")

    for str_data in [
        "Someone (My address) [e.mail@provided.by]",
        42,
    ]:
        print()

        print(f"{str_data = }")

        try:
            parse(str_data)

        except Exception as e:
            print(type(e).__name__, ':', e)
