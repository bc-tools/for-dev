#!/usr/bin/env python3

###
# This module defines constants and the interface like class ``AbstractSpeaker``
# that defines a minimal contract for speakers and also some common methods.
###


from abc import ABCMeta, abstractmethod


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# -- INTERFACE - AUTO CODE - START -- #

CONTEXT_CRITICAL = "critical"
CONTEXT_ERROR    = "error"
CONTEXT_FOCUS    = "focus"
CONTEXT_NORMAL   = "normal"
CONTEXT_WARNING  = "warning"

ALL_CONTEXTS = [
    CONTEXT_CRITICAL,
    CONTEXT_ERROR,
    CONTEXT_FOCUS,
    CONTEXT_NORMAL,
    CONTEXT_WARNING
]

# -- INTERFACE - AUTO CODE - END -- #

GLOBAL_STYLE_BW    = "balck & white"
GLOBAL_STYLE_COLOR = "color"

ALL_GLOBAL_STYLES = [
    GLOBAL_STYLE_BW,
    GLOBAL_STYLE_COLOR,
]


# -------------------------------- #
# -- ABSTRACT / INTERFACE CLASS -- #
# -------------------------------- #

###
# This abstract class / interface defines the common ¨api of the speakers.
###

class AbstractSpeaker(metaclass = ABCMeta):
# Source to have a real interface:
#     * https://realpython.com/python-interface/#using-abcabcmeta
    @classmethod
    def __subclasshook__(cls, subclass) -> None:
        goodinterface = all(
            hasattr(subclass, methodname)
            and
            callable(getattr(subclass, methodname))
            for methodname in [
                'print',
                'NL',
            ]
        )

        return goodinterface

###
# prototype::
#     style    : a global style for the output.
#              @ style in ALL_GLOBAL_STYLES
#     maxwidth : the max width expected for hard wrapped contents.
###
    def __init__(
        self,
        termstyle: str,
        maxwidth : int = 80
    ) -> None:
        self.maxwidth  = maxwidth
        self.termstyle = termstyle


###
# prototype::
#     text : a text to add as it.
#
#     :action: this method must print `text` in the output wanted.
###
    @abstractmethod
    def print(self, text: str,) -> None:
        raise NotImplementedError

###
# prototype::
#     repeat : the number of empty lines wanted.
#
#     :action: this method must print `repeat` empty lines in the output wanted.
###
    @abstractmethod
    def NL(self, repeat: int = 1) -> None:
        raise NotImplementedError


###
# prototype::
#     context : a context for formatting ¨infos.
#             @ context in ALL_CONTEXTS
#
#     :action: this methods must activate the style given when instantiating
#              the class.
#
# note::
#     This method doesn't need to be implemented (some speaker has no style
#     like the log like ones).
###
    def style(self, context: str = CONTEXT_NORMAL) -> None:
# Help for debuging.
#         print(self.__class__)
        ...


###
# prototype::
#     text : a text to be hard wrapped.
#     tab  : a possible tabulation to use for each new line created.
#
#     :return: a wrapped message of maximal width ``self.maxwidth``.
###
    def hardwrap(
        self,
        text: str,
        tab : str = ""
    ) -> str:
        shortlines = []

        for oneline in text.split('\n'):
            words = [w.strip() for w in oneline.split(' ')]

            if shortlines:
                lastline = tab

            else:
                lastline = ""

            lastline += words.pop(0)


            while(words):
                oneword = words.pop(0)

                len_lastline = len(lastline)
                len_word     = len(oneword)

                if len_lastline + len_word >= self.maxwidth :
                    shortlines.append(lastline)
                    lastline = tab

                else:
                    lastline += " "

                lastline += oneword

            shortlines.append(lastline)

        return "\n".join(shortlines)
