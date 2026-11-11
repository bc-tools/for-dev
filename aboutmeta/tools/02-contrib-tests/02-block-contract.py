#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.logconf  import *
from cbutils.contrib  import *
from cbutils.pathplus import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

NUM_TESTS = 3

CONTEXT  = 'block'
MSG_CTXT = f'{CONTEXT} contrib tests'


THIS_DIR    = Path(__file__).parent
PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'aboutmeta'):
    PROJECT_DIR = PROJECT_DIR.parent

CONTRIB_DIR = (
      PROJECT_DIR / 'contribute' / 'api'
    / 'block-n-flavour' / CONTEXT
)

CONTRIB_TESTS_DIR = CONTRIB_DIR / 'tests'

TESTS_DIR = PROJECT_DIR / 'tests' / 'api' / f'{NUM_TESTS:02}-{CONTEXT}' / 'contribs'


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

for _ in [
    add_missing_dir,
    empty_dir,
]:
    _(TESTS_DIR)

for folder, contribs in get_accepted_paths(
    context     = CONTEXT,
    contrib_dir = CONTRIB_DIR
).items():
    ctxt = folder.parent.name

    logging.info(f"Working on '{ctxt}' test data.")

    for one_contrib in sorted(contribs):
        contrib_name      = Path(one_contrib).stem
        contrib_test_data = CONTRIB_TESTS_DIR / contrib_name
        unit_test_data    = TESTS_DIR / contrib_name

        for kind in [
            'ok',
            'ko',
        ]:
            add_missing_dir(unit_test_data / kind)

        for p in contrib_test_data.glob('*/*.yaml'):
            test_file = TESTS_DIR / p.relative_to(CONTRIB_TESTS_DIR)

            content = ('\n' + ' '*2).join(
                  [f'{contrib_name}:']
                + p.read_text().split('\n')
            )

            create_update_file(
                file    = test_file,
                content = content,
            )
