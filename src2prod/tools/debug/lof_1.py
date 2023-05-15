#!/usr/bin/env python3

from cbdevtools import *


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

import src

print(dir(src))
exit()
from src import *

MONOREPO_DIR = MODULE_DIR.parent

projectname = 'src2prod'
# projectname = 'spkpb'

project = Project(
    project = MONOREPO_DIR,
    source  = Path(projectname) / 'src',
    target  = '',
    ignore  = '''
        tool_*/
        tools_*/

        tool_*.*
        tools_*.*

        test_*/
        tests_*/

        test_*.*
        tests_*.*
    ''',
    usegit = True
)

project.build()

print('---')

for f in project.lof:
    print(f)
