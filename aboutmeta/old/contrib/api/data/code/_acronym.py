#!/usr/bin/env python3

from dataclasses import dataclass

from aboutmeta.core.dataprinter import DataPrinter


# ------------------- #
# -- MY DATA CLASS -- #
# ------------------- #

@dataclass(frozen = True)
class MyDataClass(DataPrinter):
    ...


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Nothing to test!
    ...
