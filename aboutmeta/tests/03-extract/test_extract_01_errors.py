#!/usr/bin/env python3

import pytest

from aboutmeta.amdata import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

XTRCT = AMData()

THIS_DIR = Path(__file__).parent

BAD_DIR = THIS_DIR / "bad"


NB_BAD_KEYS = 3
NB_BAD_VALS = 3
NB_BAD_ALTS = 1

# ------------- #
# -- ILLEGAL -- #
# ------------- #

def test_extract_no_file_KO():
    with pytest.raises(FileNotFoundError):
        XTRCT.build(Path('bidon'))


@pytest.mark.parametrize(
    "filenb",
    range(1, NB_BAD_KEYS + 1)
)
def test_extract_unknown_key_KO(filenb):
    bad_yaml = BAD_DIR / "key" / f"{filenb}.yaml"

    with pytest.raises(
        KeyError,
        match = r"unknown key .*"
    ):
        XTRCT.build(bad_yaml)


@pytest.mark.parametrize(
    "filenb",
    range(1, NB_BAD_VALS + 1)
)
def test_extract_bad_val_type_KO(filenb):
    bad_yaml = BAD_DIR / "val" / f"{filenb}.yaml"

    with pytest.raises(
        ValueError,
        match = r"content of ''.*'' must be a .*"
    ):
        XTRCT.build(bad_yaml)


@pytest.mark.parametrize(
    "filenb",
    range(1, NB_BAD_ALTS + 1)
)
def test_extract_bad_val_type_KO(filenb):
    bad_yaml = BAD_DIR / "alt" / f"{filenb}.yaml"

    with pytest.raises(
        ValueError,
        match = r"just use on the keys .*"
    ):
        XTRCT.build(bad_yaml)
