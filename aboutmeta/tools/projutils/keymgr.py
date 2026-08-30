#!/usr/bin/env python3

from .constants import *


SPECIAL_SUFFIXES = [
    f" {s}"
    for s in "+*"
]

SPECIAL_SEPS = list(",|")


def get_mainkey(key: str) -> str:
    if key[-2:] in SPECIAL_SUFFIXES:
        key = key[:-2]

    for sep in SPECIAL_SEPS:
        if sep in key:
            key = key.split(sep)[0]
            key = key.strip()
            break

    return key
