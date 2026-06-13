#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib     import Path

from aboutmeta.core.dataprinter import DataPrinter


# ---------------------------- #
# -- TOC PATH(S) DATA CLASS -- #
# ---------------------------- #

###
# prototype::
#     std        : the standard version of the given \yaml data.
#     postsearch : ''None'', or the path to a folder containing
#                  an path::''about.yaml'' file to be analyzed
#                  during the post-production.
#     paths      : a list of paths, even if only one file has been
#                  specified (this will simplify future processing).
#                @ postsearch != None <==> paths == []
#
#
# note::
#     The ''std'' attribute is part of the frozen dataclass
#     ''DataPrinter''.
###
@dataclass(frozen = True)
class TOCPath(DataPrinter):
    postsearch: Path | None
    paths     : list[Path]


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Nothing to test!
    ...
