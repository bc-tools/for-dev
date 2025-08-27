#!/usr/bin/env python3

# from rich import print

from cbutils.yaml_blocks   import *
from cbutils.yaml_flavours import *


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

def create_codes_from_yaml(
    context,
    this_dir,
    contrib_dir_name,
    nb_step,
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
        nb_step           = nb_step,
        subfolder        = subfolder,
    )

    allfiles = get_accepted_paths(
        context    = context,
        contribdir = contribdir,
        statusdir  = statusdir,
        subfolder  = context,
        ext        = 'yaml',
    )

# Nothing added...
    if not allfiles:
        logging.warning("No file found!")

# We have to work.
    else:
        builder = (
            build_block_pycodes
            if context == "block" else
            build_flavour_pycodes
        )

        builder(
            context    = context,
            srcdir     = srcdir,
            yaml_files = allfiles,
            projdir    = projdir,
            testsdir   = testsdir,
        )
