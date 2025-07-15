#!/usr/bin/env python3

import pytest

from aboutmeta.parser.person.default import parser


# ----------- #
# -- LEGAL -- #
# ----------- #

@pytest.mark.parametrize(
    (
        "firstnames",
        "surname",
        "email",
        "affiliation"
    ),
    [
        (['A', 'B'], "C", "a.b.c@d.e", "fgh"),
        (['A', 'B'], "C", "a.b.c@d.e", ""   ),
        (['A', 'B'], "C", "a.b.c@d.e", ""   ),
        (['A', 'B'], "C", ""         , "fgh"),
        (['A', 'B'], "C", ""         , ""   ),
        ([]        , "C", ""         , ""   ),
    ]
)
def test_parser_person_default_OK(
    firstnames,
    surname,
    email,
    affiliation
):
    someone = ','.join(firstnames)

    if not firstnames:
        firstnames = None

    if someone:
        someone += ','


    someone += f"{surname}"

    if email:
        someone += f"[{email}]"

    else:
        email = None

    if affiliation:
        someone += f"({affiliation})"

    else:
        affiliation = None

    person_data = parser(someone)

    assert firstnames  == person_data.firstnames
    assert surname     == person_data.surname
    assert email       == person_data.email
    assert affiliation == person_data.affiliation


# ------------- #
# -- ILLEGAL -- #
# ------------- #

@pytest.mark.parametrize(
    "someone",
    [
        "A(B)[C]",
        "ABC)",
        "AB(C",
        "AB](C)",
        "A[B(C)",
    ]
)
def test_parser_person_default_KO(someone):
    with pytest.raises(ValueError):
        parser(someone)
