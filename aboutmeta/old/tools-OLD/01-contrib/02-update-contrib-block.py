#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.core    import *
from cbutils.yaml2py import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR          = Path(__file__).parent
PROJECT_DIR       = THIS_DIR.parent.parent
SRC_DIR           = PROJECT_DIR / "src" / "aboutmeta" / "specs"
BLOCK_CONTRIB_DIR = PROJECT_DIR / "contrib" / "block-n-flavour" / "block" / "config"


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

add_missing_init(SRC_DIR)

for folder, contribs in get_accepted_paths(PROJECT_DIR).items():
    if folder != BLOCK_CONTRIB_DIR:
        continue


# Gérer codename | doctitle *: . car doctitle disparait
    for one_contrib in contribs:
        logging.info(f"Working on '{one_contrib}'.")

        contrib_file = folder / one_contrib

        d = digested_yaml_specs(contrib_file)

        from pprint import pprint;pprint(d)
