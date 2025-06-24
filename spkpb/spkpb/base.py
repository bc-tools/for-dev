#!/usr/bin/env python3

from typing import *

from pathlib import Path

from .problems import *
from .timer    import *


# ------------------------------ #
# -- BASE COMMUNICATING CLASS -- #
# ------------------------------ #

###
# This class gives the common interface for classes working with "speakers"
# and "problems".
###
class BaseCom:

###
# prototype::
#     problems : an instance of ''toolbox.Problems'' that manages
#                a basic history of the problems found.
#
# note::
#     This class uses the attribut ''success'' to indicate if
#     at least one "critical" or error has been emitted (sometimes
#     we want to continue to work even if something bad has been
#     found, for example when working on several projects in the
#     same monorepo)
###
    def __init__(
        self,
        problems: Problems,
    ) -> None:
        self.problems = problems
        self.success  = True


###
# prototype::
#     :see: problems.Problems.reset ,
#           speaker.allinone.Speaker.reset
#
# This method is just an easy-to-use wrapper to reset the log file,
# the attributs used to manage the problems and also the numbering
# of steps.
###
    def reset(self) -> None:
        self.problems.reset()


###
# prototype::
#     :see: problems.Problems.new_warning
#
# This method is just an easy-to-use wrapper.
###
    def new_warning(self, *args, **kwargs):
        self.problems.new_warning(*args, **kwargs)

###
# prototype::
#     :see: problems.Problems.new_warning
#
# This method is just an easy-to-use wrapper.
#
# note::
#     The difference between a warning and a critical is that a critical is
#     a warning that blocks one part of the process but not all the process.
#     It is a kind of weak error or very strong warning.
###
    def new_critical(self, *args, **kwargs):
        self.success = False
        self.problems.new_critical(*args, **kwargs)

###
# prototype::
#     :see: problems.Problems.new_error
#
# This method is just an easy-to-use wrapper.
###
    def new_error(self, *args, **kwargs):
        self.success = False
        self.problems.new_error(*args, **kwargs)

###
# prototype::
#     :see: problems.Problems.resume
#
# This method is just an easy-to-use wrapper.
###
    def resume(self, *args, **kwargs):
        self.problems.resume(*args, **kwargs)


###
# prototype::
#     :see: speaker.allinone.Speaker.recipe
#
# This method is just an esay-to-use wrapper.
###
    def recipe(self, *args, **kwargs) -> None:
        self.problems.speaker.recipe(*args, **kwargs)


###
# prototype::
#     kind    : the kind of time stamp ("start" and "end" for example).
#               This string will be always "upperized".
#     with_NL : ''True'' asks to add a new line after the title and
#               ''False'' to not do this.
#
#     :see: timer.timestamp
#
# This method is just an easy-to-use wrapper.
###
    def timestamp(
        self,
        kind   : str,
        with_NL: bool = True
    ):
        timestamp(
            speaker = self.problems.speaker,
            kind    = kind,
            with_NL = with_NL,
        )
