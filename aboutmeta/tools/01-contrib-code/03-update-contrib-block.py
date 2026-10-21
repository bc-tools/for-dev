#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.logconf    import *
from cbutils.pathplus   import *
from cbutils.coding_py  import *



# ------------------ #
# -- CONSTANTS #1 -- #
# ------------------ #

CONTEXT  = 'block'
MSG_CTXT = 'block config contrib'


THIS_DIR    = Path(__file__).parent
PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'aboutmeta'):
    PROJECT_DIR = PROJECT_DIR.parent

SPECS_DIR       = PROJECT_DIR / 'src' / 'aboutmeta' / 'specs'
BLOCK_SPECS_DIR = SPECS_DIR / CONTEXT
CONTRIB_DIR     = PROJECT_DIR / 'contribute' / 'api' / 'block-n-flavour' / CONTEXT




# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

for f in [
    empty_dir,
    add_missing_init,
]:
    f(BLOCK_SPECS_DIR)


exit()

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
