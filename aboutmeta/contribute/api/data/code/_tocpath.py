#!/usr/bin/env python3

from dataclasses import field

from pathlib import Path

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ---------- #
# -- DATA -- #
# ---------- #

###
# prototype::  A  REVOIR
#     spec : the specification of YYYY
#     XXXX : XXXX
###
class TOCPath(DataManager):
    spec : str | dict(str, str)
    paths: dict(str, str | Path) = field(init = False)


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Nothing to test!
    ...
