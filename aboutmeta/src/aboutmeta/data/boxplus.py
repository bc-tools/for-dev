#!/usr/bin/env python3

from box import Box


# ---------- #
# -- XXXXXXXXXXXXXXX -- #
# ---------- #

### TODO
# prototype::
#     content : XXX
#
#     :return: XXX
###
class BoxPlus(Box):
    def __call__(
        self,
        str_attrs
    ):
        val = self

        for n in str_attrs.split('.'):
            val = getattr(val, n)

        return val
