#!/usr/bin/env python3

import pytest

from aboutmeta.parser.license.default import parser


# ----------- #
# -- LEGAL -- #
# ----------- #

@pytest.mark.parametrize(
    (
        "strict_ID",
        "lazzy_ID"
    ),
    [
        ("GPL-3.0+"    , "gpl - 3.0 +"    ),
        ("CC-BY-NC-4.0", "cc    by nc 4.0"),
    ]
)
def test_parser_license_default_OK(
    strict_ID,
    lazzy_ID
):
    lic_data = parser(lazzy_ID)

    assert strict_ID == lic_data.std


# ------------- #
# -- ILLEGAL -- #
# ------------- #

@pytest.mark.parametrize(
    "lazzy_ID",
    [
        "gpl",
        "cc nc"
    ]
)
def test_parser_license_default_KO(lazzy_ID):
    with pytest.raises(ValueError):
        parser(lazzy_ID)
