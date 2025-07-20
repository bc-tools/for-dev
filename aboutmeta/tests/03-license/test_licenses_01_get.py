#!/usr/bin/env python3

import pytest

from aboutmeta.tool.license import get_licence_text


# ----------- #
# -- LEGAL -- #
# ----------- #

# https://raw.githubusercontent.com/spdx/license-list-data/main/text/GPL-3.0+.txt
# https://raw.githubusercontent.com/spdx/license-list-data/main/text/CC-BY-NC-4.0.txt"

@pytest.mark.parametrize(
    (
        "lic_ID",
        "line_1"
    ),
    [
        (
            "GPL-3.0-only",
            "GNU GENERAL PUBLIC LICENSE"
        ),
        (
            "CC-BY-NC-4.0",
            "Creative Commons Attribution-NonCommercial 4.0 International"
        ),
    ]
)
def test_get_licenses_OK(lic_ID, line_1):
    text = get_licence_text(lic_ID)

    line_1_found = text.split('\n')[0]

    assert line_1 == line_1_found




# ------------- #
# -- ILLEGAL -- #
# ------------- #

@pytest.mark.parametrize(
    "lic_ID",
    [
        "X",
        "gpl - 3.0 +",
    ]
)
def test_get_licenses_KO(lic_ID):
    with pytest.raises(
        FileNotFoundError,
        match = r"bad SPDX_ID:.*"
    ):
        get_licence_text(lic_ID)
