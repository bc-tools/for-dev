#!/usr/bin/env python3

import pytest

from aboutmeta.parser.license.default import parser


# ----------- #
# -- LEGAL -- #
# ----------- #

def test_parser_license_default_OK():
    for strict_ID, lazzy_ID in [
        ("GPL-3.0+"    , "gpl - 3.0 +"),
        ("CC-BY-NC-4.0", "cc    by nc 4.0"),
    ]:
        lic_data = parser(lazzy_ID)

        assert strict_ID == lic_data.std, f"license tested: {lazzy_ID}"


# ------------- #
# -- ILLEGAL -- #
# ------------- #

def test_parser_license_default_KO():
    for lazzy_ID in [
        "gpl",
        "cc nc"
    ]:
        with pytest.raises(ValueError):
            parser(lazzy_ID)
