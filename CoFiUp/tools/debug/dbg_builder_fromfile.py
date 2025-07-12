#! /usr/bin/env python3

from pathlib import Path
from pprint  import pprint

from cbdevtools import *


# Clear the terminal.
print("\033c", end="")


# ------------------------------------ #
# -- MODULES IMPORTED FROM SOURCES! -- #
# ------------------------------------ #

addfindsrc(
    file    = __file__,
    project = 'CoFiUp',
)

from src import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_FILE = Path(__file__)
THIS_DIR  = Path(THIS_FILE).parent

PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'CoFiUp'):
   PROJECT_DIR = PROJECT_DIR.parent

TESTS_OUT_DIR = PROJECT_DIR / 'tests' / 'outputs'


# --------------------- #
# -- PLAYING WITH... -- #
# --------------------- #

kind     = "exadoc"
mychoice = "about2pyproj-1"
mychoice = "about2pyproj-2"


folder_tested = TESTS_OUT_DIR / kind / mychoice

cfg_cfup = folder_tested / "cfg.cfup.yaml"


# ------------------ #
# -- WHAT WE WANT -- #
# ------------------ #

print("Playing with...")
print(f"{cfg_cfup}")

with open(cfg_cfup, mode='r') as file:
    yaml_data = yaml.load(file, Loader=yaml.BaseLoader)

print(yaml_data)
