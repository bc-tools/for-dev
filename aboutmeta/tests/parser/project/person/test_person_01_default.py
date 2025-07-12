#!/usr/bin/env python3

import pytest

from aboutmeta.parser.project.person.default import parser


# ----------- #
# -- LEGAL -- #
# ----------- #

def test_parser_person_default_OK():
    for firstnames, surname, email, affiliation in [
        (
            ['A', 'B'],
            "C",
            "a.b.c@d.e",
            "fgh",
        ),
        (
            ['A', 'B'],
            "C",
            "a.b.c@d.e",
            "",
        ),
        (
            ['A', 'B'],
            "C",
            "a.b.c@d.e",
            "",
        ),
        (
            ['A', 'B'],
            "C",
            "",
            "fgh",
        ),
        (
            ['A', 'B'],
            "C",
            "",
            "",
        ),
        (
            [],
            "C",
            "",
            "",
        ),
    ]:
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

        assert firstnames  == person_data.firstnames, f"person tested: {someone}"
        assert surname     == person_data.surname, f"person tested: {someone}"
        assert email       == person_data.email, f"person tested: {someone}"
        assert affiliation == person_data.affiliation, f"person tested: {someone}"


# ------------- #
# -- ILLEGAL -- #
# ------------- #

def test_parser_person_default_KO():
    for someone in [
        "ABC)",
        "AB(C",
        "AB](C)",
        "A[B(C)"
    ]:
        with pytest.raises(ValueError):
            parser(someone)
