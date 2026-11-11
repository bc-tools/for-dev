#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.amdata      import *

from aboutmeta.specs.block.__ALL_BLOCKS__ import ALL_BLOCKS

import pytest


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR          = Path(__file__).parent
CONTRIB_TESTS_DIR = THIS_DIR / 'contribs'

TAG_OK = 'ok'
TAG_KO = 'ko'

GLOB_ABOUT_SEARCH = '*/*about.yaml'


# --------------------- #
# -- GOOD STRUCTURES -- #
# --------------------- #

def test_good_yaml_structure() -> None:
    for bname in ALL_BLOCKS:
        contrib_tests = CONTRIB_TESTS_DIR / bname / TAG_OK

        for one_about in contrib_tests.glob(GLOB_ABOUT_SEARCH):
            amdata = AMData.new_instance(
                flavour = [bname],
                parent  = one_about.parent,
            )

            amdata.build(no_parsing = True)


# -------------------- #
# -- BAD STRUCTURES -- #
# -------------------- #

def test_good_yaml_structure() -> None:
    for bname in ALL_BLOCKS:
        contrib_tests = CONTRIB_TESTS_DIR / bname / TAG_KO

        for one_about in contrib_tests.glob(GLOB_ABOUT_SEARCH):
            amdata = AMData.new_instance(
                flavour = [bname],
                parent  = one_about.parent,
            )

            with pytest.raises((KeyPathError, ValueError)):
                amdata.build(no_parsing = True)
