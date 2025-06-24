#!/usr/bin/env python3

from cbdevtools import *

# projectname = 'spkpb'
# projectname = 'cbdevtools'
projectname = 'monorepo'
# projectname = 'multimd'
projectname = 'src2prod'
projectname = 'jinjaNG'


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

MONOREPO_DIR = MODULE_DIR.parent
PROJECT_DIR  = Path(projectname)

project = Project(
    project = MONOREPO_DIR / PROJECT_DIR,
    src  = 'src',
    dest  = projectname.lower(),
    ignore  = MONOREPO_DIR / 'ignore-for-prod.txt',
    usegit  = True,
    # readme  = 'README.md',
    readme  = 'readme',
)

project.build(erase = False)
