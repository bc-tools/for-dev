#!/usr/bin/env python3

###
# This module defines the internal class ''TermSpeaker'' to "speak" on
# a terminal.
#
# note::
#     There are also two classes ''BWStylist'' and ''ColorStylist'' to
#     produce the style wanted.
###


from enum import Enum

from .spk_interface import *


# -------------- #
# -- STYLISTS -- #
# -------------- #

###
# prototype::
#     value    : the style code choosen.
#     codetemp : a template that will be updated with the value of
#                the style code.
#     normcode : the code for the normal style.
#
# This function is just a basic factorization for coding the stylists.
###

def _colorit(
    value   : str,
    codetemp: str,
    normcode: str,
) -> None:
    if value:
        termcode = codetemp.format(value = value)

    else:
        termcode = normcode

    print(termcode, end = "")


###
# This class "colorizes" easily the terminal outputs.
###

# Source: GNU/Linux Mag. - Hors Série 115

class ColorStylist(Enum):
# See ''spk_interface.ALL_CONTEXTS.''
    normal  : str = ''
    good    : str = '96'
    warning : str = '94'
    critical: str = '95'
    error   : str = '31'

    def colorit(self) -> None:
        _colorit(
            value    = self.value,
            codetemp = '\x1b[1;{value}m',
            normcode = '\x1b[0m'
        )

###
# This class uses a "black and white" style for the terminal outputs.
###

class BWStylist(Enum):
# See ''spk_interface.ALL_CONTEXTS.''
    normal  : str = ''
    good    : str = '1m'
    warning : str = '3m'
    critical: str = '1m'
    error   : str = '3m\033[1m'

    def colorit(self) -> None:
        _colorit(
            value    = self.value,
            codetemp = '\033[{value}',
            normcode = '\033[0m'
        )


# ------------------ #
# -- TERM SPEAKER -- #
# ------------------ #

###
# This class implements methods to print ¨infos on the terminal.
###

class TermSpeaker(AbstractSpeaker):
###
# prototype::
#     style    : a global style for the outputs.
#              @ :in: spk_interface.ALL_GLOBAL_STYLES
#     maxwidth : the maw width expected for hard wrapped contents.
###
    def __init__(
        self,
        style,
        maxwidth: int = 80
    ) -> None:
        super().__init__(
            termstyle    = style,
            maxwidth = maxwidth
        )

        self.stylist = {
            GLOBAL_STYLE_COLOR: ColorStylist,
            GLOBAL_STYLE_BW   : BWStylist
        }[self.termstyle]


###
# prototype::
#     repeat : the numebr of empty lines wanted.
#
# This method simply prints ''repeat'' empty lines on the terminal.
###
    def NL(self, repeat: int = 1) -> None:
        print("\n"*(repeat - 1))

###
# prototype::
#     text : a text to print as it on the terminal.
###
    def print(self, text: str) -> None:
        print(text)

###
# prototype::
#     context : a context to format some outputs
#             @ :in: spk_interface.CONTEXTS
#
#     :see: = ''ColorStylist'' and ''BWStylist''.
###
    def style(self, context: str = CONTEXT_NORMAL) -> None:
        getattr(self.stylist, context).colorit()


###
# prototype::
#     text : a text to be hard wrapped.
#     tab  : a possible tabulation to use for each new line created.
#
#     :return: a wrapped message of maximal width ''self.maxwidth''.
#
# note::
#     We redefine the method ''hardwrap'' because in a terminal, the
#     hard wrapping consists only to add tabulations "to" each new line.
###
    def hardwrap(
        self,
        text: str,
        tab : str = ""
    ) -> str:
        lines = text.split('\n')

        return f'\n{tab}'.join(lines)
