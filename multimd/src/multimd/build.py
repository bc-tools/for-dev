#!/usr/bin/env python3

###
# This module allows to make a single \md file from several single ones
# (using or not an "automatic" merging).
###


from pathlib import Path

from .about    import *
from .finalize import stdit


# -------------------------------- #
# -- SINGLE \MD FROM \MD CHUNKS -- #
# -------------------------------- #

###
# This class finds all the single \md files and then builds a final
# single one with all the chunks found.
###
class Builder:
###
# prototype::
#     src   : the path of the \dir containing the \md chunks.
#     dest  : the path of the single final \md file to build.
#     erase : set to ''True'', this \arg allows to erase an existing
#             final file to build a new one.
###
    def __init__(
        self,
        src  : Path,
        dest : Path,
        erase: bool = False
    ) -> None:
        self.src   = src
        self.dest  = dest
        self.erase = erase

###
# prototype::
#     :action: this method finds the single \md files, and then merges
#              all the \md codes found to build the final \md file.
###
    def build(self) -> None:
# All the \md codes.
        mdcode = []

        for onefile in TOC(self.src).extract():
            mdcode.append(
                onefile.read_text(encoding = "utf-8").strip()
            )

        mdcode = ("\n" * 3).join(mdcode)

# Can we erase an existing final file?
        if self.dest.is_file() and not self.erase:
            raise IOError(
                f"the class {type(self).__name__} is not allowed "
                "to erase the final file:"
                "\n"
                f"{self.dest}"
            )

        mdcode += "\n"

# User's \md single version.
        self.dest.write_text(
            data     = mdcode,
            encoding = "utf-8"
        )

# Standard version.
        stdit(
            self.dest,
            self.dest,
            erase = True
        )
