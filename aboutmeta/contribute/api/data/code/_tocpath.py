#!/usr/bin/env python3

from dataclasses import field

import fnmatch
import re

from pathlib import Path

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ---------- #
# -- DATA -- #
# ---------- #

###
# prototype::
#     spec : YYYY
###
class TOCPath(DataManager):
    spec: dict[str, str]

###
# prototype::
#     :action: XXXX
###
    def __post_init__(self) -> None:
        ...




def valider_syntaxe_glob(pattern: str) -> bool:
    """Vérifie si un motif glob est syntaxiquement valide."""
    try:
        # translate() convertit le glob en regex, re.compile() valide la regex
        regex_str = fnmatch.translate(pattern)
        re.compile(regex_str)
        return True
    except (re.error, TypeError):
        return False

# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Nothing to test!
    ...
