#!/usr/bin/env python3

from typing import List

from dataclasses import dataclass

from .constants  import *


# -------------------- #
# -- URL DATA CLASS -- #
# -------------------- #

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

###  TODO
# prototype::
#     :return: list of errors detected.
#
# note::
#     As the validation system is not 100% reliable, we can
#     only return a list of errors detected (with possible
#     false negatives). This choice also allows us to produce
#     a final report of everything that has not been validated,
#     thus saving the user from having to spend time studying
#     problems one by one.
###
    def validate(self) -> List[str]:
        print(f"??? {self.url}")
