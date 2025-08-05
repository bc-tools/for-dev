#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib     import Path

from aboutmeta.core.dataprinter import *


# ----------------- #
# -- TOC PATH(S) -- #
# ----------------- #

### TODO
# prototype::
#     data : str | dict[str, str]
#     kind : str
#     paths: Path | list[Path]
###
@dataclass(frozen = True)
class TOCPath(DataPrinter):
    data : str | dict[str, str]
    kind : str
    paths: Path | list[Path]

###
# The string representation is the user's data with escaped characters.
###
    def __str__(self) -> str:
# One-key dict used in the initial ''YAML'' file.
        if isinstance(self.data, dict):
            for k, v in self.data.items():
                return f"{k}: '{v}'"

# One string used in the initial ''YAML'' file.
        return self.data
