#!/usr/bin/env python3


# ------------- #
# -- PARSING -- #
# ------------- #

###
# Parsing errors must use the ''ParsingError'' class.
#
#
# note::
#     What was the idea behind the text above? :-) Sorry about
#     that, but I'll stick to using dummy explanations for now.
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


###
# Bad YAML data type must use the ''YAMLTypeError'' class.
###
class YAMLTypeError(Exception):
    ...

###
# Critical implementation errors must use the ''PostProcessingError'' class.
###
class CriticalImplementationError(Exception):
    def __init__(
        self,
        msg: str
    ) -> None:
        msg = (
            f'{msg} Please REPORT this critical bug '
            'with minimal amount of data for testing.'
        )

        super().__init__(msg)


# --------------------- #
# -- NOTHING TO TEST -- #
# --------------------- #
