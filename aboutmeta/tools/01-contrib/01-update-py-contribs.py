#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from utilities.cnp_code import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent

CONTRIBS_INFOS = [
#   (context    , contrib_dir_name)
    (CTXT_DATA  , CTXT_DATA),
    (CTXT_PARSER, CTXT_PARSER),
    (CTXT_MAPPER, CTXT_PARSER),
]

NBTEST_START = 1


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

for nbtest, (context, contrib_dir_name) in enumerate(
    CONTRIBS_INFOS,
    start = NBTEST_START
):
    if nbtest != NBTEST_START:
        print()

    copy_paste_codes(
        context          = context,
        this_dir         = THIS_DIR,
        contrib_dir_name = contrib_dir_name,
        nbtest           = nbtest,
    )
