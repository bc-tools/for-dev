#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from utilities.cnp_code   import *
from utilities.need_tests import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

CONTRIB_CTXT    = CTXT_MAPPER
CONTRIB_FOLDER  = CTXT_PARSER
CONTRIB_NB_TEST = Path(__file__).name.split('-')[0]

THIS_DIR    = Path(__file__).parent
CONTRIB_DIR = Path(__file__).parent


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

contexts_added = copy_paste_codes(
    this_dir    = THIS_DIR,
    contrib_dir = CONTRIB_FOLDER,
    context     = CONTRIB_CTXT,
)

if contexts_added:
    missing_unit_tests(
        this_dir       = THIS_DIR,
        contrib_dir    = CONTRIB_FOLDER,
        context        = CONTRIB_CTXT,
        nb_test        = CONTRIB_NB_TEST,
        contexts_added = contexts_added
    )
