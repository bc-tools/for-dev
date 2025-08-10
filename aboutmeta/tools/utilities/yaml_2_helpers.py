#!/usr/bin/env python3

from rich import print

from utilities.cnp_code import *


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

def build_helpers(
    context,
    this_dir,
    contrib_dir_name,
    nbtest,
    subfolder,
):
    (
        projdir,
        projname,
        contribdir,
        statusdir,
        srcdir,
        testsdir
    ) = get_specs_folders(
        context          = context,
        this_dir         = this_dir,
        contrib_dir_name = contrib_dir_name,
        nbtest           = nbtest,
        subfolder        = subfolder,
    )

    allfiles = get_accepted_paths(
        context    = context,
        contribdir = contribdir,
        statusdir  = statusdir,
        subfolder  = context,
        ext        = 'yaml',
    )

    print(allfiles)
