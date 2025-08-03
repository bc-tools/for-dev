#!/usr/bin/env python3


# ----------------------- #
# -- PRINTER INTERFACE -- #
# ----------------------- #

###
# This interface just implements the magic ''__str__'' method to print
# the string attribute ''std''.
#
# note::
#     The ''std'' attribute will be used as a "normalized" version in
#     the path::''about.yaml'' file.
###
class DataPrinter:
    def __str__(self) -> str:
        return self.std
