#!/usr/bin/env python3

import pytest

from aboutmeta.parser.lang.default import parser


# ----------- #
# -- LEGAL -- #
# ----------- #

def test_parser_lang_default_OK():
    for lazzy_ID, strict_ID in [
        ("fr"   , "fr-FR"),
        ("es"   , "es-ES"),
        ("en"   , "en-US"),
        ("de"   , "de-DE"),
        ("en-GB", "en-GB"),
    ]:
        lang_data = parser(lazzy_ID)

        assert strict_ID == lang_data.std, f"lazzy lang ID tested: {lazzy_ID}"


# ------------- #
# -- ILLEGAL -- #
# ------------- #

def test_parser_lang_default_KO():
    for lazzy_ID in [
        "XX",
        "XXXXXX",
    ]:
        with pytest.raises(ValueError):
            parser(lazzy_ID)
