#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.yaml_2_helpers import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent

CONTRIBS_INFOS = [
    ("block"  , "block-n-flavour"),
    ("flavour"  , "block-n-flavour"),
]

NB_STEP_START = 6


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

for nb_step, (context, contrib_dir_name) in enumerate(
    CONTRIBS_INFOS,
    start = NB_STEP_START
):
    if nb_step != NB_STEP_START:
        print()

    build_helpers(
        context          = context,
        this_dir         = THIS_DIR,
        contrib_dir_name = contrib_dir_name,
        nb_step           = nb_step,
        subfolder        = context,
    )
