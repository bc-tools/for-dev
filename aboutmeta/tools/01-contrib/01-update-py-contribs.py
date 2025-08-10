#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from utilities.cnp_code   import *
from utilities.need_tests import *


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


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

for nbtest, (context, contrib_dir_name) in enumerate(
    CONTRIBS_INFOS,
    start = 1
):
    if nbtest != 1:
        print()

    copy_paste_codes(
        context          = context,
        this_dir         = THIS_DIR,
        contrib_dir_name = contrib_dir_name,
        nbtest           = nbtest,
    )
