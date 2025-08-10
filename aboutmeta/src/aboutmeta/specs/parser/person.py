#!/usr/bin/env python3

from aboutmeta.core.constants    import *
from aboutmeta.core.errors       import ParsingError
from aboutmeta.specs.data.person import Person
from aboutmeta.tool.group        import (
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
        content   = titles[-1].strip(),
        delims    = DELIMS_PARTICLE,
        context   = "surname",
        left_most = False
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
        std         = std,
        firstnames  = firstnames,
        surname     = (particle, main_name),
        email       = email,
        affiliation = affiliation
    )
