#!/usr/bin/env python3

from pathlib import Path
import              pytest

from aboutmeta.extract import Extract


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR      = Path(__file__).parent
PROJECT_DIR   = THIS_DIR.parent.parent
PROJECT_ABOUT = PROJECT_DIR / "about.yaml"

XTRCT = Extract()


# ------------- #
# -- LEGAL -- #
# ------------- #

def test_extract_data_OK():
    data = XTRCT.build(PROJECT_ABOUT)
