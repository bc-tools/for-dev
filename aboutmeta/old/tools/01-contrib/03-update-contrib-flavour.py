#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.core    import *
from cbutils.yaml2py import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR    = Path(__file__).parent
PROJECT_DIR = THIS_DIR.parent.parent
SRC_DIR     = PROJECT_DIR / "src" / "aboutmeta" / "specs"
CONTRIB_DIR = PROJECT_DIR / "contrib" / "block-n-flavour" / "flavour" / "config"


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

for folder, contribs in get_accepted_paths(PROJECT_DIR).items():
    if folder != CONTRIB_DIR:
        continue

    print(contribs)
