#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.logconf    import *
from cbutils.pathplus   import *
from cbutils.coding_py  import *
from cbutils.contrib    import *

from projutils.yaml2py import *


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


# ----------- #
# -- TOOLS -- #
# ----------- #



# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

for f in [
    empty_dir,
    add_missing_init,
]:
    f(BLOCK_SPECS_DIR)


for folder, contribs in get_accepted_paths(
    context     = CONTEXT,
    contrib_dir = CONTRIB_DIR
).items():
    ctxt = folder.parent.name

    logging.info(f"Working on '{ctxt}' configs.")

    for one_contrib in contribs:
        logging.info(f"Analyzing '{one_contrib}'.")

        contrib_file = folder / one_contrib

        digested_yaml = DigestedYamlSpecs(contrib_file)
        digested_yaml.build()

# DEBUG - START
        from pprint import pprint
        print('---')
        pprint(digested_yaml.specs)
        print('---')
        print(digested_yaml.status.to_json(indent=4))
        print('---')
        print(digested_yaml.alts)#.to_json(indent=4))
        # exit()
# DEBUG - END
