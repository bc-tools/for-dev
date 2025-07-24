#!/usr/bin/env python3

from typing import List

from dataclasses import dataclass
from pathlib     import Path


# ----------------- #
# -- TOC PATH(S) -- #
# ----------------- #

###
# Easy-to-use data class for ''toc'' paths.
###
@dataclass
class TOCPath:
    data : str | dict[str, str]
    kind : str
    paths: Path | List[Path]

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
