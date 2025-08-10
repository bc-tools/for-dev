#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from utilities.yaml_2_helpers import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent

CONTRIBS_INFOS = [
#   (context    , contrib_dir_name)
    ("block"  , "block-n-flavour"),
    ("flavour"  , "block-n-flavour"),
]

NBTEST_START = 6


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

# for nbtest, (context, contrib_dir_name) in enumerate(
#     CONTRIBS_INFOS,
#     start = NBTEST_START
# ):
#     if nbtest != NBTEST_START:
#         print()

#     create_codes_from_yaml(
#         context          = context,
#         this_dir         = THIS_DIR,
#         contrib_dir_name = contrib_dir_name,
#         nbtest           = nbtest,
#         subfolder        = context,
#     )
