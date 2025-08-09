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
    nbtest,
    codes_added
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
        nbtest,
    )

    testsdir_rel = testsdir.relative_to(projdir)

    logging.info(f"Verification of ''{testsdir_rel}''.")

# Test files implemented.
    codes_added  = codes_added
    contexts_tested = {
        tf.name
        for tf in testsdir.glob("**/test_*.py")
    }

# No problem.
    if codes_added == contexts_tested:
        logging.info(f"Nothing to declare.")

    else:
# Missing tests?
        print_pbs(
            context = context,
            tests   = codes_added - contexts_tested,
            kind    = "missing",
            level   = TAG_CRITICAL,
        )

# Extra tests?
        print_pbs(
            context = context,
            tests   = contexts_tested - codes_added,
            kind    = "extra",
            level   = TAG_WARNING,
        )


def print_pbs(
    context,
    tests,
    kind,
    level
):
    if tests:
        log_print = (
            logging.warning
            if level == TAG_WARNING else
            logging.critical
        )

        plurial = '' if len(tests) == 1 else 's'

        log_print(
            log_title(
                title = f"{context} testing",
                desc  = f"{kind.title()} one{plurial}."
            )
        )

        for t in sorted(list(tests)):
            log_print(f"{t}.")
