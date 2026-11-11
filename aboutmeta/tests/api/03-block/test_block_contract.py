#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.amdata import *

import pytest


# --------------------- #
# -- XXXX -- #
# --------------------- #

BLOCK_2_FLAVOUR = dict()

for flavour, specs in ALL_FLAVOURS.items():
    for block in specs:
        if not block in BLOCK_2_FLAVOUR:
            BLOCK_2_FLAVOUR[block] = flavour





print(BLOCK_2_FLAVOUR)




# --------------------- #
# -- GOOD STRUCTURES -- #
# --------------------- #





# -------------------- #
# -- BAD STRUCTURES -- #
# -------------------- #
