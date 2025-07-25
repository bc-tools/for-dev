#!/usr/bin/env python3

from typing import Any

from box import Box


# ---------------------- #
# -- BETTER BOX CLASS -- #
# ---------------------- #

###
# We make the class ''Box'' callable to allow the use of virtual
# pointed paths. For example, you can use ''myboxobj("a.b.c.d")''
# instead of ''myboxobj.a.b.c.d''.
###
class BoxPlus(Box):
###
# prototype::
#     content : a pointed path instead of sequence of attributes.
#
#     :return: the expected value (if it exists).
###
    def __call__(
        self,
        str_attrs: str
    ) -> Any:
        val = self

        for n in str_attrs.split('.'):
            val = getattr(val, n)

        return val
