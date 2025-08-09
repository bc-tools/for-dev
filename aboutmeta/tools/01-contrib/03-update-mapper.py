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

codes_added = copy_paste_codes(
    this_dir    = THIS_DIR,
    contrib_dir = CONTRIB_FOLDER,
    context     = CONTRIB_CTXT,
)

if codes_added:
    missing_unit_tests(
        this_dir    = THIS_DIR,
        contrib_dir = CONTRIB_FOLDER,
        context     = CONTRIB_CTXT,
        nbtest      = CONTRIB_NB_TEST,
        codes_added = codes_added
    )
