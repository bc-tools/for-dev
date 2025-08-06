#!/usr/bin/env python3

from dataclasses import dataclass


# ----------------------- #
# -- PRINTER INTERFACE -- #
# ----------------------- #

###
# prototype::
#     std : this attribute will be used to store a "standard"
#           version of the data in the path::''about.yaml'' file.
#           This attribute is also used for basing printing.
#
#
# important::
#     Do not confuse standard version with normalized version.
#     In some cases, data can be validated in an atypical form
#     and then normalized. See, for example, the ''data.url.URL''
#     class.
###
@dataclass(frozen = True)
class DataPrinter:
    std: str

###
# The magic method ''__str__'' should just display the string
# attribute ''std''.
###
    def __str__(self) -> str:
        return self.std
