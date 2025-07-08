#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class License:
    std : str
    name: str
    ref : str

    def __str__(self):
        return self.std
