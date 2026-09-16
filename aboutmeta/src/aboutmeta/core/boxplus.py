#!/usr/bin/env python3

from typing import Any

from box import Box


# ------------------------ #
# -- ENHANCED BOX CLASS -- #
# ------------------------ #

###
# We make the class ''Box'' callable to allow the use of virtual
# pointed paths. For example, you can use ''myboxobj("a.b.c.d")''
# instead of ''myboxobj.a.b.c.d''.
###
class BoxPlus(Box):
###
# prototype::
#     attrs : a pointed path instead of sequence of attributes.
#
#     :return: the expected value (if it exists).
###
    def __call__(
        self,
        attrs: str
    ) -> Any:
        val = self

        for oneattr in attrs.split('.'):
            val = getattr(val, oneattr)

        return val
