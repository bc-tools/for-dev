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

from src import *

for kind in [
    'auto',
    'reverse',
]:
    print(f'    + {kind}')

    Builder(
        src   = THIS_DIR / f'build-{kind}',
        dest  = THIS_DIR / f'build-{kind}-final.md',
        erase = True,
    ).build()
