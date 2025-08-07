#!/usr/bin/env python3

from utilities import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

CONTRIB_FOLDER  = CONTRIB_CTXT = CTXT_PARSER
CONTRIB_NB_TEST = Path(__file__).name.split('-')[0]

THIS_DIR = Path(__file__).parent


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

print(f"{ITEM_1} Creation/update of source code...")

copy_paste_files(
    this_dir    = THIS_DIR,
    contrib_dir = CONTRIB_FOLDER,
    context     = CONTRIB_CTXT,
    nb_test     = CONTRIB_NB_TEST
)
