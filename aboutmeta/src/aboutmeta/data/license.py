#!/usr/bin/env python3

from dataclasses import dataclass


# ------------------------ #
# -- LICENSE DATA CLASS -- #
# ------------------------ #

### TODO
# prototype::
#     content : XXX
#
#     :return: XXX
###
@dataclass
class License:
    std : str
    name: str
    ref : str

###
# We want to string print the standard code of the license.
###
    def __str__(self):
        return self.std
