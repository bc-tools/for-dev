#!/usr/bin/env python3

from aboutmeta.core.constants    import *
from aboutmeta.core.errors       import ParsingError
from aboutmeta.specs.data.person import Person
from aboutmeta.tools.group       import (
    extract_group,
    gather_groups
)


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

# It remains to build the standard version.
    if particle is None:
        std = f"{main_name}"

    else:
        std = f"{{{particle}}} {main_name}"

    if firstnames:
        firstnames = ', '.join(firstnames)
        std        = f"{firstnames}, {std}"

    std = gather_groups(
        groups = [
            std,
            "" if email is None else email,
            "" if affiliation is None else affiliation,
        ],
        delims = DELIMS_PERSON,
    )

# The job has been done.
    return Person(
        yaml_val    = std,
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
# We just need some basic interface tests, because we have already
# tested the ''Person'' class.

# GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    print()

    str_data    = "ALIce,    MarIE-LiSe,   {DE}    Charlène   [   a.b.c@d.e ](fgh  )"
    data_parsed = parse(str_data)

    print(str_data)
    print(repr(data_parsed))

# BAD
    # exit()

    print("\n------------\n")

    print("-- BAD CASES --")

    print()

    try:
        str_data = 42

        print(str_data)
        parse(str_data)

    except Exception as e:
        print(type(e).__name__, ':', e)
