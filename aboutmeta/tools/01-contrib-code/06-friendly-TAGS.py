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

THIS_DIR    = Path(__file__).parent
PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'aboutmeta'):
    PROJECT_DIR = PROJECT_DIR.parent

SPECS_DIR = PROJECT_DIR / 'src' / 'aboutmeta' / 'specs'

THIS_FILE_RELATIVE = (
      Path('aboutmeta')
    / Path(__file__).relative_to(PROJECT_DIR)
)


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

logging.info(f"Working on 'friendly key tags'.")

# Post-processing tags.

# Block names and data keys.

# Sort tags and use emty lines when chnagin first letters (leadin underscores ignored).
