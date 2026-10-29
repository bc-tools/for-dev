#!/usr/bin/env python3


# ------------- #
# -- PARSING -- #
# ------------- #

###
# Parsing errors must use the ''ParsingError'' class.
#
#
# note::
#     Why was the above written? :-)
###
class ParsingError(Exception):
    ...


###
# Parsing key paths errors must use the ''KeyPathError'' class.
###
class KeyPathError(Exception):
    ...


###
# Post processing errors must use the ''PostProcessingError'' class.
###
class PostProcessingError(Exception):
    ...


# --------------------- #
# -- NOTHING TO TEST -- #
# --------------------- #
