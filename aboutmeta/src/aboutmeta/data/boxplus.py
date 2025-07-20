#!/usr/bin/env python3

from box import Box


# ---------------------- #
# -- BETTER BOX CLASS -- #
# ---------------------- #

###
# We make the class ''Box'' callable to allow the use of
# virtual pointed paths.
###
class BoxPlus(Box):
###
# prototype::
#     content : a pointed path similar to a sequence of
#               attributes request.
#
#     :return: the expected value.
###
    def __call__(
        self,
        str_attrs
    ):
        val = self

        for n in str_attrs.split('.'):
            val = getattr(val, n)

        return val
