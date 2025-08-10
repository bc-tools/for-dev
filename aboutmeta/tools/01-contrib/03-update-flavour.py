#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from utilities.yaml_flavours import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

CONTRIB_CTXT    = "flavour"
CONTRIB_FOLDER  = "block-n-flavour"
CONTRIB_NB_TEST = 2 + int(Path(__file__).name.split('-')[0])

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
    build_flavour_pycodes(
        context    = CONTRIB_CTXT,
        srcdir     = srcdir,
        yaml_files = allfiles,
        projdir    = projdir,
        testsdir   = testsdir,
    )
