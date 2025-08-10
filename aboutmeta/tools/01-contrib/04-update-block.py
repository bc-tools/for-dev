#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from utilities.cnp_code   import *
from utilities.need_tests import *
from utilities.yaml2code  import *

# --------------- #
# -- CONSTANTS -- #
# --------------- #

CONTRIB_CTXT    = "block"
CONTRIB_FOLDER  = "block-n-flavour"
CONTRIB_NB_TEST = Path(__file__).name.split('-')[0]

THIS_DIR    = Path(__file__).parent
CONTRIB_DIR = Path(__file__).parent


# ------------------ #
# -- YAML TO CODE -- #
# ------------------ #

logging.info(f"Codes for {CONTRIB_CTXT}: creation or update.")

(
    projdir,
    projname,
    contribdir,
    statusdir,
    srcdir,
    testsdir
) = get_folders(
    this_dir    = THIS_DIR,
    contrib_dir = CONTRIB_FOLDER,
    context     = CONTRIB_CTXT,
    nbtest      = CONTRIB_NB_TEST,
    subfolder   = CONTRIB_CTXT,
)

allfiles = get_accepted_paths(
    contribdir,
    statusdir,
    subfolder = CONTRIB_CTXT,
    ext       = 'yaml',
)

codes_added = build_block_pycodes(
    context    = CONTRIB_CTXT,
    srcdir     = srcdir,
    yaml_files = allfiles,
)

if codes_added:
    missing_unit_tests(
        this_dir    = THIS_DIR,
        contrib_dir = CONTRIB_FOLDER,
        context     = CONTRIB_CTXT,
        nbtest      = CONTRIB_NB_TEST,
        codes_added = codes_added
    )
