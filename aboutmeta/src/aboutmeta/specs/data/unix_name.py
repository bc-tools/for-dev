#!/usr/bin/env python3

# Code extracted from the maintained file
# aboutmeta/contribute/api/data/code/unix_name.py

import re


from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ---------- #
# -- DATA -- #
# ---------- #

PATTERN_UNIX_NAME = re.compile(r'^[a-z_][a-z0-9_-]*$')


###
# prototype::
#     name : a Unix-style name that only uses lowercase letters,
#            digits, underscores, and hyphens, and cannot start
#            with a digit or a hyphen.
###
class UnixName(DataManager):
    name: str

###
# prototype::
#     :action: mandatory validation of the Unix name.
###
    def __post_init__(self) -> None:
        if not PATTERN_UNIX_NAME.match(self.name):
            raise ParsingError(f'Unvalid Unix name "{name}".')
