#!/usr/bin/env python3

from cbdevtools import *


# ------------------------------------ #
# -- MODULES IMPORTED FROM SOURCES! -- #
# ------------------------------------ #

MODULE_DIR = addfindsrc(
    file    = __file__,
    project = 'multimd',
)

THIS_DIR = Path(__file__).parent


# -------------- #
# -- LET'S GO -- #
# -------------- #

from src.toc import TOC

for kind in [
    'all-files',
]:
    print(f'-- {kind} --')

    for onepath in TOC(
        THIS_DIR / f'about-{kind}'
    ).extract():
        print(onepath)

    print()
