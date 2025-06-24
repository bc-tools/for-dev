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
    project = 'jinjaNG',
)

from src.jngbuild import *


# ----------------- #
# -- WHAT WE USE -- #
# ----------------- #

VERBOSE = False
# VERBOSE = True

CONFIG = NO_CONFIG
# CONFIG = AUTO_CONFIG
# CONFIG = "mycfg.yaml"

FILES_FOLDER_NB = "01"


DATA_EXT = "yaml"
# DATA_EXT = "json"
# DATA_EXT = "py"

KIND = DATA_EXT
# KIND = "hooks"

LAUNCH_PY = True
# LAUNCH_PY = False

TEMPL_EXT = "txt"
# TEMPL_EXT = "tex"


# -------------- #
# -- LET'S GO -- #
# -------------- #

THIS_FILE = Path(__file__)
THIS_DIR  = Path(THIS_FILE).parent

FILES_FOLDER_NAME = f"{KIND}-{FILES_FOLDER_NB}"
FILES_FOLDER      = THIS_DIR / "files" / FILES_FOLDER_NAME

template = FILES_FOLDER / f"template.{TEMPL_EXT}"
output   = FILES_FOLDER / f"output.{TEMPL_EXT}"
data     = FILES_FOLDER / f"data.{DATA_EXT}"

if CONFIG in [NO_CONFIG, AUTO_CONFIG]:
    config = CONFIG

else:
    config = FILES_FOLDER / CONFIG


print(f"Working on {FILES_FOLDER = }")
print()

JNGBuilder(
    launch_py = LAUNCH_PY,
    config    = config,
    verbose   = VERBOSE,
).render(
    data     = str(data),
    template = str(template),
    output   = str(output),
)


print(
    f"Rendering from {DATA_EXT.upper()} made in "
    f"the folder ''files/{FILES_FOLDER_NAME}''."
)

print()
