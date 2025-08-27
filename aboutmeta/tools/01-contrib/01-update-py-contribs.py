#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.core import *

from cbutils.cnp_code import *


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

NB_STEP_START = 1


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

for nb_step, (context, contrib_dir_name) in enumerate(
    CONTRIBS_INFOS,
    start = NB_STEP_START
):
    if nb_step != NB_STEP_START:
        print()

    copy_paste_codes(
        context          = context,
        this_dir         = THIS_DIR,
        contrib_dir_name = contrib_dir_name,
        nb_step           = nb_step,
    )
