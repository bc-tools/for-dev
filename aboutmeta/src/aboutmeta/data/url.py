#!/usr/bin/env python3

from typing import List

from dataclasses import dataclass

from .constants  import *


# ----------------------- #
# -- PERSON DATA CLASS -- #
# ----------------------- #

###
# Easy-to-use data class for URLs.
###
@dataclass
class URL:
    url: str

###
# The string representation is be a normalized version using
# the syntax of the path::''about.yaml''.
###
    def __str__(self) -> str:
        return self.url

###
# XXX
###
    def validate(self):
        ...
