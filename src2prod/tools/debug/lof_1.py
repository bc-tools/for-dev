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


from src_OLD import *
from src     import *

MONOREPO_DIR = MODULE_DIR.parent

projectname = 'src2prod'
# projectname = 'spkpb'

project = Project(
    project = MONOREPO_DIR,
    src  = Path(projectname) / 'src',
    dest  = '',
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

project.check()

print('---')

for f in project.lof:
    print(f)
