#!/usr/bin/env python3

from pprint import pprint

from collections import defaultdict

from .common import *


# --------------------------- #
# -- FILES FOR UNIT TESTS? -- #
# --------------------------- #

def missing_unit_tests(
    this_dir,
    contrib_dir,
    context,
    nb_test,
    contexts_added
):
    (
        projdir,
        projname,
        contribdir,
        statusdir,
        srcdir,
        testsdir
    ) = get_folders(
        this_dir,
        contrib_dir,
        context,
        nb_test,
    )

    testsdir_rel = testsdir.relative_to(projdir)

    logging.info(f"Verification of ''{testsdir_rel}''.")

# Test files implemented.
    contexts_added  = contexts_added
    contexts_tested = {
        tf.parent.name
        for tf in testsdir.glob("**/test_*.py")
    }

# No problem.
    if contexts_added == contexts_tested:
        logging.info(f"Nothing to declare.")

    else:
# Missing tests?
        print_pbs(
            context = context,
            tests   = contexts_added - contexts_tested,
            kind    = "missing"
        )

# Extra tests?
        print_pbs(
            context = context,
            tests   = contexts_tested - contexts_added,
            kind    = "extra"
        )


def print_pbs(
    context,
    tests,
    kind
):
    if tests:
        plurial = '' if len(tests) == 1 else 's'

        logging.error(
            log_title(
                title = context,
                desc  = f"{kind.title()} test{plurial}."
            )
        )

        for t in sorted(list(tests)):
            logging.error(f"{t}.")
