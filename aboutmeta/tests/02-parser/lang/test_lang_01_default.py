#!/usr/bin/env python3

import pytest

from aboutmeta.parser.lang.default import parser


# ----------- #
# -- LEGAL -- #
# ----------- #

@pytest.mark.parametrize(
    (
        "lazzy_ID",
        "strict_ID"
    ),
    [
        ("fr"   , "fr-FR"),
        ("es"   , "es-ES"),
        ("en"   , "en-US"),
        ("de"   , "de-DE"),
        ("en-GB", "en-GB"),
    ]
)
def test_parser_lang_default_OK(
    lazzy_ID,
    strict_ID
):
    lang_data = parser(lazzy_ID)

    assert strict_ID == lang_data.std


# ------------- #
# -- ILLEGAL -- #
# ------------- #

@pytest.mark.parametrize(
    "lazzy_ID",
    [
        "XX",
        "XXXXXX",
    ]
)
def test_parser_lang_default_KO(lazzy_ID):
    with pytest.raises(ValueError):
        parser(lazzy_ID)
