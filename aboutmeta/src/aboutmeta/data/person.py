#!/usr/bin/env python3

from typing import List

from dataclasses import dataclass

from .constants  import *

import logging

# ----------------------- #
# -- PERSON DATA CLASS -- #
# ----------------------- #

###
# Easy-to-use data class for persons.
###
@dataclass
class Person:
    firstnames : List[str]
    surname    : str
    email      : str
    affiliation: str

###
# The string representation must be a normalized version using
# the syntax of the path::''about.yaml''.
###
    def __str__(self) -> str:
        text = self.surname

        if self.firstnames:
            firstnames = ', '.join(self.firstnames)
            text       = f"{firstnames}, {text}"

        if self.email:
            text += f' {TAG_YAML_EMAIL_OPEN}{self.email}{TAG_YAML_EMAIL_CLOSE}'

        if self.affiliation:
            text += f' {TAG_YAML_AFFILIATION_OPEN}{self.affiliation}{TAG_YAML_AFFILIATION_CLOSE}'

        return text

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
    def validate(self) -> int:
        print(f"??? {self.email}")
        print(f"??? {self.affiliation}")

        return 0
