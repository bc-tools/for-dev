#!/usr/bin/env python3

from cbdevtools import *

projectname = 'TeXitEasy'
projectname = 'TeXfactory'


# ------------------------------------ #
# -- MODULES IMPORTED FROM SOURCES! -- #
# ------------------------------------ #

MODULE_DIR = addfindsrc(
    file    = __file__,
    project = 'src2prod',
)


# -------------- #
# -- LET'S GO -- #
# -------------- #

from src_OLD import *
from src     import *

MONOREPO_DIR = MODULE_DIR.parent.parent / 'for-latex'
PROJECT_DIR  = MONOREPO_DIR / Path(projectname)

project = Project(
    project = PROJECT_DIR,
    src  = 'src',
    dest  = projectname.lower(),
    ignore  = MONOREPO_DIR / 'ignore-for-prod.txt',
    usegit  = True,
    readme  = 'readme'
)

project.build(erase = False)
