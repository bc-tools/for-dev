#!/usr/bin/env python3

from typing import List

from dataclasses import dataclass

from .constants  import *

@dataclass
class Person:
    firstnames : List[str]
    surname    : str
    email      : str
    affiliation: str

    def __str__(self):
        text = self.surname

        if self.firstnames:
            text = f"{', '.join(self.firstnames)}, {text}"

        if self.email:
            text += f' {TAG_EMAIL_OPEN}{self.email}{TAG_EMAIL_CLOSE}'

        if self.affiliation:
            text += f' {TAG_AFFILIATION_OPEN}{self.affiliation}{TAG_AFFILIATION_CLOSE}'

        return text
