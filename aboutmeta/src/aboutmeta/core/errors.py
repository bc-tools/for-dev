#!/usr/bin/env python3


# ------------- #
# -- PARSING -- #
# ------------- #

###
# For parsing errors.
#
#
# note::
#     What was the idea behind the text above? :-) Sorry about
#     that, but I'll stick to using dummy explanations for now.
###
class ParsingError(Exception):
    ...


###
# For parsing key paths errors.
###
class KeyPathError(Exception):
    ...


# ---------------- #
# -- PROCESSING -- #
# ---------------- #

###
# For post processing errors.
###
class PostProcessingError(Exception):
    ...


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# For critical implementation errors.
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
