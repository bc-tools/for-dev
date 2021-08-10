#!/usr/bin/env python3

from pathlib import Path
import sys


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent


# ------------------------------------ #
# -- MODULES IMPORTED FROM SOURCES! -- #
# ------------------------------------ #

PROJECT_NAME = 'spkpb'
MODULE_DIR   = THIS_DIR

if not PROJECT_NAME in str(MODULE_DIR):
    raise Exception(
        "call the script from a working directory containing the project."
    )

while(not MODULE_DIR.name.startswith(PROJECT_NAME)):
    MODULE_DIR = MODULE_DIR.parent

sys.path.append(str(MODULE_DIR))


# -------------- #
# -- LET'S GO -- #
# -------------- #

from src import *

speaker = Speaker(
    logfile = Path('mylog.log')
)

timestamp(
    speaker = speaker,
    kind    = 'start 1',
)

timestamp(
    speaker = speaker,
    kind    = 'start 2',
    with_NL = False,
)

timestamp(
    speaker = speaker,
    kind    = 'start 3',
)