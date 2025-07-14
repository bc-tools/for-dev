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


NB_BAD_KEYS = 3 + 1

@pytest.mark.parametrize("i", range(1, NB_BAD_KEYS))
def test_extract_unknown_key_KO(i):
    bad_yaml = BAD_DIR / "key" / f"{i}.yaml"

    with pytest.raises(KeyError):
        XTRCT.build(bad_yaml)
