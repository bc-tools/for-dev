#!/usr/bin/env python3

# from pprint import pprint

from utilities.cnp_code import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #



# ------------- #
# -- PY CODE -- #
# ------------- #

def build_flavour_pycodes(
    context,
    srcdir,
    yaml_files,
    projdir,
    testsdir,
):
    logging.info(
       f"{context.upper()} - Validating YAML contribs."
    )
