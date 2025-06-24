#!/usr/bin/env python3

###
# This module defines the internal class ''LogSpeaker'' to "speak" in
# a log file.
###


from pathlib import Path

from .spk_interface import *


# ----------------- #
# -- LOG SPEAKER -- #
# ----------------- #

###
# This class implements methods to print ¨infos in the log file.
###

class LogSpeaker(AbstractSpeaker):
###
# prototype::
#     logfile  : the path of the log file.
#     style    : a global style for the outputs.
#              @ :in: spk_interface.ALL_GLOBAL_STYLES
#     maxwidth : the max width expected for hard wrapped contents.
###
    def __init__(
        self,
        logfile : Path,
        style   : str,
        maxwidth: int,
    ) -> None:
        super().__init__(
            termstyle    = style,
            maxwidth = maxwidth
        )

        self.logfile = logfile

        self.reset_logfile()

###
# This method produces a new empty log file.
###
    def reset_logfile(self) -> None:
# Empty an existing log file.
        if self.logfile.is_file():
            with self.logfile.open(
                encoding = "utf8",
                mode     = "w"
            ) as logfile:
                logfile.write("")

# New log file if it doesn't exist.
        else:
            self.logfile.touch()


###
# prototype::
#     text : a text to print as it in the log file.
###
    def print(
        self, text  : str,
    ) -> None:
        with self.logfile.open(
            encoding = "utf8",
            mode     = "a"
        ) as logfile:
            logfile.write(text)
            logfile.write("\n")


###
# prototype::
#     repeat : the number of empty lines wanted.
#
# This method simply append ''repeat'' empty new lines to the log file.
###
    def NL(self, repeat: int = 1) -> None:
        self.print("\n"*(repeat - 1))
