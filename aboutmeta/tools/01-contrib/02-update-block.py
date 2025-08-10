#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from utilities.cnp_code  import *
from utilities.yaml2code import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

CONTRIB_CTXT    = "block"
CONTRIB_FOLDER  = "block-n-flavour"
CONTRIB_NB_TEST = 4

THIS_DIR    = Path(__file__).parent
CONTRIB_DIR = Path(__file__).parent


# ------------------ #
# -- YAML TO CODE -- #
# ------------------ #

(
    projdir,
    projname,
    contribdir,
    statusdir,
    srcdir,
    testsdir
) = get_folders(
    context          = CONTRIB_CTXT,
    this_dir         = THIS_DIR,
    contrib_dir_name = CONTRIB_FOLDER,
    nbtest           = CONTRIB_NB_TEST,
    subfolder        = CONTRIB_CTXT,
)

allfiles = get_accepted_paths(
    context    = CONTRIB_CTXT,
    contribdir = contribdir,
    statusdir  = statusdir,
    subfolder  = CONTRIB_CTXT,
    ext        = 'yaml',
)

# Nothing added...
if not allfiles:
    logging.warning("No file found!")

# We have to work.
else:
    codes_added = build_block_pycodes(
        context    = CONTRIB_CTXT,
        srcdir     = srcdir,
        yaml_files = allfiles,
    )

    if codes_added:
        missing_unit_tests(
            context     = CONTRIB_CTXT,
            codes_added = codes_added,
            projdir     = projdir,
            testsdir    = testsdir,
        )
