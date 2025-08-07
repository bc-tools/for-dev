#!/usr/bin/env python3

# from pprint import pprint

from pathlib     import Path
import                  re


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAB_1 = ' '*2
TAB_2 = TAB_1*2
TAB_3 = TAB_1*3

ITEM_1 = '+'
ITEM_2 = f'{TAB_1}*'
ITEM_3 = f'{TAB_2}-'
ITEM_4 = f'{TAB_3}-->'


# ----------- #
# -- PATHS -- #
# ----------- #

def get_folders(
    this_dir,
    contrib_dir,
    context,
    nbtest,
):
    projdir  = this_dir.parent.parent
    projname = projdir.name

    contribdir = projdir / "contrib" / contrib_dir / "code"
    statusdir  = contribdir.parent / "status"
    srcdir     = projdir / "src" / projname / context
    testsdir   = projdir / "tests" / f"{nbtest}-{context}"

    return (
        projdir,
        projname,
        contribdir,
        statusdir,
        srcdir,
        testsdir
    )
