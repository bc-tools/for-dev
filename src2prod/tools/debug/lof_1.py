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

PROJECT_NAME = 'src2prod'
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
