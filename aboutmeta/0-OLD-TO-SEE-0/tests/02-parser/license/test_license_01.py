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
        ("GPL-3.0-only", "gpl - 3.0   only   "),
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
        "cc nc",
    ]
)
def test_parser_license_default_UNKNOWN(lazzy_ID):
    with pytest.raises(
        ValueError,
        match = "unknown license code.*"
    ):
        parser(lazzy_ID)


@pytest.mark.parametrize(
    "lazzy_ID",
    [
        "gpl 3.0 +",
    ]
)
def test_parser_license_default_DEPRECATED(lazzy_ID):
    with pytest.raises(
        ValueError,
        match = "deprecated license code.*"
    ):
        parser(lazzy_ID)
