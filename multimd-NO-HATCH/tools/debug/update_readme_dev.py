#!/usr/bin/env python3

from cbdevtools import *

projectname = 'about'
projectname = 'cleanit'
projectname = 'multimd'
projectname = 'src2prod'
# projectname = 'jinjaNG'


# ------------------------------------ #
# -- MODULES IMPORTED FROM SOURCES! -- #
# ------------------------------------ #

MODULE_DIR = addfindsrc(
    file    = __file__,
    project = 'multimd',
)

MONOREPO_DIR = MODULE_DIR.parent
PROJECT_DIR  = MONOREPO_DIR / Path(projectname)


# -------------- #
# -- LET'S GO -- #
# -------------- #

from src import *

Builder(
    src   = PROJECT_DIR / 'readme',
    dest  = PROJECT_DIR / 'README.md',
    erase = True,
).build()
