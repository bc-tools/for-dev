#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib     import Path

from aboutmeta.core.dataprinter import DataPrinter


# ----------------- #
# -- TOC PATH(S) -- #
# ----------------- #

###
# prototype::
#     std        : the standard version of the given \yaml data
#                  which can be normalized in the case of a
#                  hard-coded path.
#     postsearch : ''None'', or the path to a folder containing
#                  an path::''about.yaml'' file to be analyzed
#                  during the post-production.
#                @ paths != [] ==> postsearch == None
#     paths      : a list of paths, even if only one file has been
#                  specified (this will simplify future processing).
#                @ postsearch != None ==> paths == []
###
@dataclass(frozen = True)
class TOCPath(DataPrinter):
    std       : str
    postsearch: Path | None
    paths     : list[Path]
