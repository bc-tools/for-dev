#!/usr/bin/env python3

from cbdevtools import *


# ------------------------------------ #
# -- MODULES IMPORTED FROM SOURCES! -- #
# ------------------------------------ #

MODULE_DIR = addfindsrc(
    file    = __file__,
    project = 'spkpb',
)


# -------------- #
# -- LET'S GO -- #
# -------------- #

from src import *

speaker = Speaker()
