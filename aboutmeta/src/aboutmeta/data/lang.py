#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class Lang:
    std      : str
    name     : str
    territory: str

    def __str__(self):
        return self.std
