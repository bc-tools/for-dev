#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib     import Path


# ----------------- #
# -- TOC PATH(S) -- #
# ----------------- #

###
# Easy-to-use data class for ''toc'' paths.
###
@dataclass(frozen = True)
class TOCPath:
    std        : str
    recusearch : Path | None
    paths      : list[Path]
