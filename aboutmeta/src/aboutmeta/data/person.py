#!/usr/bin/env python3

from typing import List

from dataclasses import dataclass

from .constants  import *


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
    def __str__(self):
        text = self.surname

        if self.firstnames:
            firstnames = ', '.join(self.firstnames)
            text       = f"{firstnames}, {text}"

        if self.email:
            text += f' {TAG_YAML_EMAIL_OPEN}{self.email}{TAG_YAML_EMAIL_CLOSE}'

        if self.affiliation:
            text += f' {TAG_YAML_AFFILIATION_OPEN}{self.affiliation}{TAG_YAML_AFFILIATION_CLOSE}'

        return text

###
# XXX
###
    def validate(self):
        ...
