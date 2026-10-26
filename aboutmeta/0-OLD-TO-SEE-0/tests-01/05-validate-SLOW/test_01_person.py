#!/usr/bin/env python3

import pytest

from aboutmeta.parser.person.default import parser
from aboutmeta.data.person           import Person


# ----------- #
# -- LEGAL -- #
# ----------- #

@pytest.mark.parametrize(
    ("someone"),
    [
        "Mr, Nobody",
        "Mr, Nobody (Google, USA)",
        "Mr, Nobody [mr-nobody@gmail.com]",
        "Mr, Nobody [mr-nobody@gmail.com] (Google, USA)",
    ]
)
def test_person_validation_OK(someone):
    someone = parser(someone)

    assert someone.validate() == 0


# ------------- #
# -- ILLEGAL -- #
# ------------- #

@pytest.mark.parametrize(
    (
        "someone",
        "nb_pbs"
    ),
    [
        (
            "Mr, Nobody (Ggle, USA)",
            1
        ),
        (
            "Mr, Nobody [mr-nobody@gamcom]",
            1
        ),
        (
            "Mr, Nobody [mr-nobody@gamcom] (Ggle, USA)",
            2
        ),
    ]
)
def test_person_validation_KO(someone, nb_pbs):
    someone = parser(someone)

    assert someone.validate() == nb_pbs
