#!/usr/bin/env python3

import pytest

from aboutmeta.data.url import URL


# ----------- #
# -- LEGAL -- #
# ----------- #

@pytest.mark.parametrize(
    "url",
    [
        "https://google.fr",
    ]
)
def test_url_validation_OK(url):
    url_validator = URL(url = url)

    assert url_validator.validate() == 0


# ------------- #
# -- ILLEGAL -- #
# ------------- #

@pytest.mark.parametrize(
    (
        "url",
        "nb_pbs"
    ),
    [
        ("google.fr", 2),
    ]
)
def test_url_validation_KO(url, nb_pbs):
    url_validator = URL(url = url)

    assert url_validator.validate() == nb_pbs
