#!/usr/bin/env python3

import pytest

from aboutmeta.amdata import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

XTRCT = AMData()

THIS_DIR = Path(__file__).parent

TEST_DIR_NAME = "extract"

DATA_DIR    = THIS_DIR.parent / "data"
OK_DATA_DIR = DATA_DIR / "OK" / TEST_DIR_NAME
KO_DATA_DIR = DATA_DIR / "KO" / TEST_DIR_NAME


NB_BAD_KEYS = len([p for p in (KO_DATA_DIR / "key").glob("*.yaml")])
NB_BAD_VALS = len([p for p in (KO_DATA_DIR / "val").glob("*.yaml")])
NB_BAD_ALTS = len([p for p in (KO_DATA_DIR / "alt").glob("*.yaml")])


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
    bad_yaml = KO_DATA_DIR / "key" / f"{filenb}.yaml"

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
    bad_yaml = KO_DATA_DIR / "val" / f"{filenb}.yaml"

    with pytest.raises(
        ValueError,
        match = r"content of ''.*'' must be a .*"
    ):
        XTRCT.build(bad_yaml)


@pytest.mark.parametrize(
    "filenb",
    range(1, NB_BAD_ALTS + 1)
)
def test_extract_bad_alt_KO(filenb):
    bad_yaml = KO_DATA_DIR / "alt" / f"{filenb}.yaml"

    with pytest.raises(
        ValueError,
        match = r"just use on the keys .*"
    ):
        XTRCT.build(bad_yaml)
