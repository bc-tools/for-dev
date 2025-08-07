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
    print(f"{ITEM_1} Unit test analysis.")

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

# Test files implemented.
    contexts_added  = contexts_added
    contexts_tested = {
        tf.parent.name
        for tf in testsdir.glob("**/test_*.py")
    }

# No problem.
    if contexts_added == contexts_tested:
        print(f"{ITEM_2} Nothing to declare.")

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

        print(f"{ITEM_2} [{context}]  {kind.title()} test{plurial}.")

        for t in sorted(list(tests)):
            print(f"{ITEM_3} {t}.")
