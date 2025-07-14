#!/usr/bin/env python3

import pytest

from aboutmeta.extract import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

XTRCT = Extract()

THIS_DIR = Path(__file__).parent

BAD_DIR = THIS_DIR / "bad"


# ------------- #
# -- ILLEGAL -- #
# ------------- #

def test_extract_no_file_KO():
    with pytest.raises(FileNotFoundError):
        XTRCT.build(Path('bidon'))


def test_extract_unknown_key_1_KO():
    with pytest.raises(KeyError):
        XTRCT.build(AD_DIR / "key" / "1.yaml")

def test_extract_unknown_key_2_KO():
    with pytest.raises(KeyError):
        XTRCT.build(AD_DIR / "key" / "2.yaml")

def test_extract_unknown_key_3_KO():
    with pytest.raises(KeyError):
        XTRCT.build(AD_DIR / "key" / "3.yaml")
