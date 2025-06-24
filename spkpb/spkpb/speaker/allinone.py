#!/usr/bin/env python3

###
# This module defines the class ''Speaker'' that manages easy-to-use recipes
# and the wanted prints (on the terminal and/or in the log file).
###


from typing import Union

from functools import wraps
from pathlib   import Path

from mistool.term_use import ALL_FRAMES, withframe

from .log  import *
from .term import *


# -------------- #
# -- DECORATE -- #
# -------------- #

# The zero level item will never be used but it simplifies the coding
# of the API.
ITEM = [
    f'{" "*(4*i)}{deco}'
    if deco != ' ' else
    ''
    for i, deco in enumerate(" *+-")
]

TAB = [
    4*i
    for i in range(0, 4)
]


ASCII_FRAME = {}

for i in range(1, 3):
    ASCII_FRAME[i] = lambda t: withframe(
        text  = t,
        frame = ALL_FRAMES[f'pyba_title_{i}']
    )


# ------------------ #
# -- FOR RECIPES -- #
# ------------------ #

# -- RECIPES - AUTO CODE - START -- #

FORALL  = "forall"
FORLOG  = "forlog"
FORTERM = "forterm"
NL      = "NL"
PRINT   = "print"
PROBLEM = "problem"
STEP    = "step"
STYLE   = "style"
TITLE   = "title"

ACTIONS_NO_ARG = [
    FORALL,
    FORLOG,
    FORTERM,
    NL,
    STYLE,
]

VAR_CONTEXT   = "context"
VAR_INFO      = "info"
VAR_LEVEL     = "level"
VAR_PB_ID     = "pb_id"
VAR_REPEAT    = "repeat"
VAR_STEP_INFO = "step_info"
VAR_TAB       = "tab"
VAR_TEXT      = "text"
VAR_TITLE     = "title"
VAR_WITH_NL   = "with_NL"

# -- RECIPES - AUTO CODE - END -- #


# ---------------------- #
# -- SILENT DECORATOR -- #
# ---------------------- #

###
# This decorator simplifies the managment of the use of ''silent = False''
# when instanciating the class ''Speaker''.
###

def only_resume_or_not_deco(method):
    @wraps(method)
    def only_resume_or_not(self, *args, **kwargs) -> None:
        if self.onlyresume:
            self._current_outputs = []

        else:
            method(self, *args, **kwargs)

    return only_resume_or_not


# ------------- #
# -- SPEAKER -- #
# ------------- #

###
# This class is used to "speak": the ¨infos are printed on the terminal
# and in a log file.
#
# warning::
#     This class must work in any context of use!
###

class Speaker(AbstractSpeaker):
    OUTPUT_LOG  = "log"
    OUTPUT_TERM = "term"

###
# prototype::
#     logfile   : ''None'' to not use a log file, or the path of the log file.
#     style     : ''None'' to not use the terminal, or the style to use in
#                 the terminal.
#               @ :in: GLOBAL_STYLE_BW, GLOBAL_STYLE_COLOR]
#     onlyresume: ''True'' indicates to only print a resume of the errors found
#                 contrary to ''False'' (this is useful for short processes showing
#                 only warning and co when using the method ''resume'' of the class
#                 ''problems.Problems'').
###
    def __init__(
        self,
        termstyle : Union[None, str]  = None,
        logfile   : Union[None, Path] = None,
        maxwidth  : int  = 80,
        onlyresume: bool = False,
    ) -> None:
# At least one output is needed.
        if logfile is None and termstyle is None:
            raise ValueError(
                'you must use at least one of the arguments '
                '"termstyle" and "logfile".'
            )

        if termstyle:
            assert termstyle in ALL_GLOBAL_STYLES

# Here we do not need the use of ''super().__init__()''.
        self._speakers   = {}
        self._all_outputs = []

        if termstyle:
            self._all_outputs.append(self.OUTPUT_TERM)

            self._speakers[self.OUTPUT_TERM] = TermSpeaker(
                style    = termstyle,
                maxwidth = maxwidth,
            )

        if logfile:
            self._all_outputs.append(self.OUTPUT_LOG)

            self._speakers[self.OUTPUT_LOG] = LogSpeaker(
                logfile  = logfile,
                style    = termstyle,
                maxwidth = maxwidth,
            )

# Reset.
        self.onlyresume = onlyresume
        self.reset()


###
# prototype::
#     :see: speaker.log.LogSpeaker
#
# This method resets the log file and the numbering of steps.
###
    def reset(self) -> None:
        if self.OUTPUT_LOG in self._speakers:
            self._speakers[self.OUTPUT_LOG].reset_logfile()

        self.nbsteps = {
            out: 0
            for out in self._all_outputs
        }


###
# We use ''getter'' and ''setter'' for the boolean attribute ''silent''
# to automatically update the list of outputs expected.
###
    @property
    def onlyresume(self):
        return self._onlyresume

    @onlyresume.setter
    def onlyresume(self, value: bool) -> None:
        self._onlyresume = value

        if value:
            self._current_outputs = []

        else:
            self._current_outputs = self._all_outputs


###
# This method is to use only for a "LOG FILE" output.
###
    @only_resume_or_not_deco
    def forlog(self) -> None:
        if self.OUTPUT_LOG not in self._all_outputs:
            raise ValueError(
                'the "logfile" output can\'t be used with this instance of "Speaker".'
            )

        self._current_outputs = [self.OUTPUT_LOG]

###
# This method is to use only for a "TERM" output.
###
    @only_resume_or_not_deco
    def forterm(self) -> None:
        if self.OUTPUT_TERM not in self._all_outputs:
            raise ValueError(
                'the "term" output can\'t be used with this instance of "Speaker".'
            )

        self._current_outputs = [self.OUTPUT_TERM]

###
# This method is to use all outputs.
###
    @only_resume_or_not_deco
    def forall(self) -> None:
        self._current_outputs = self._all_outputs


###
# prototype::
#     repeat : the number of empty lines wanted.
#
# This method simply prints ''repeat'' empty new lines in all the
# outputs wanted.
###
    def NL(self, repeat: int = 1) -> None:
        for out in self._current_outputs:
            self._speakers[out].NL(repeat)

###
# prototype::
#     text : a text to communicate.
###
    def print(self, text: str) -> None:
        for out in self._current_outputs:
            self._speakers[out].print(text)

###
# prototype::
#     context : a context for formatting ¨infos.
#             @ :in: spk_interface.ALL_CONTEXTS
###
    def style(self, context: str = CONTEXT_NORMAL) -> None:
        for out in self._current_outputs:
            self._speakers[out].style(context)


###
# prototype::
#     title   : the content of the title.
#     level   : the level of the title.
#             @ :in: 1..2
#     with_NL : ''True'' asks to add a new line after the title and
#               ''False'' to not do this
#
# note::
#     ''with_NL'' is used to resume problems found, or to print
#     the very last time stamps in the log file.
###
    def title(self,
        title  : str,
        level  : int  = 1,
        with_NL: bool = True,
    ) -> None:
        self.print(ASCII_FRAME[level](title))

        if with_NL:
            self.NL()

###
# prototype::
#     step_info : one short info.
#     level     : the level of step indicating where ''0'' is for automatic
#                 numbered enumerations.
#               @ :in: 0..3
###
    def step(self,
        step_info: str,
        level    : int = 0,
    ) -> None:
        for out in self._current_outputs:
            item = self._stepitem(
                out   = out,
                level = level
            )

            text = self._speakers[out].hardwrap(
                text = f'{item}{step_info}',
                tab  = " "*len(item)
            )

            self._speakers[out].print(text)

###
# This method simpliy resets to `0` the number of numbered steps.
###
    def _reset_nbstep(self) -> None:
        for out in self._current_outputs:
            self.nbsteps[out] = 0

###
# prototype::
#     out   : the kind of speaker.
#     level : the level of step indicating where ''0'' is for automatic
#             numbered enumerations.
#           @ :in: 0..3
###
    def _stepitem(
        self,
        out  : str,
        level: int = 0,
    ) -> None:
# Enumeration...
        if level == 0:
            self.nbsteps[out] += 1

            return f'{self.nbsteps[out]}) '

# Basic item
        return f'{ITEM[level]} '


###
# prototype::
#     context : the context of a problem.
#     pb_id   : the number of the problem.
#     message : the message to print.
#     level   : the level of the step indicating the problem.
#             @ in 0..3
###
    def problem(
        self,
        context: str,
        pb_id  : int,
        info   : str,
        level  : int = 0
    ) -> None:
        self.style(context)

        self.step(
            step_info = f'[ #{pb_id} ] {context.upper()}: {info}',
            level     = level
        )

        self.style(CONTEXT_NORMAL)


###
# prototype::
#     *args : the classical list of args allowed by Python.
#
# This method allows to indicate recipes to apply suchas to simplify
# the "speaking". Here is an exemple of use followed by the actions
# actualy done (some actions have short version expressions).
#
# python::
#     self.speaker.receipe(
#         SPEAKER_FOR_TERM,
#         SPEAKER_NL,
#         (SPEAKER_TITLE, f'MONOREPO "{self.monorepo.name}"'),
#         {VAR_TITLE: "STARTING THE ANALYSIS",
#          VAR_LEVEL: 2}, # A short version here!
#     )
#
# This says to do the following actions.
#
# python::
#     self.speaker.forterm()
#     self.speaker.NL()
#     self.speaker.title(f'MONOREPO "{self.monorepo.name}"')
#     self.speaker.title(
#         title = "STARTING THE ANALYSIS",
#         level = 2
#     )
#
#
# note::
#     One recipe always start and finishes in an "for all" normal context.
#     This is not optimal but simplifies the writting of recipes.
###
    def recipe(self, *args) -> None:
# Default "for all" normal context.
        self.forall()
        self.style()

# In most cases, to call the good action with its good arguments we will use:
# ''getattr(self, action)(*action_args, **action_kwargs)''.
        for action in args:
# An action with no arg.
            if action in ACTIONS_NO_ARG:
                getattr(self, action)()
                continue

# Just a context.
            elif action in ALL_CONTEXTS:
                action_args   = [action]
                action_kwargs = {}
                action        = STYLE

# A "string short version" that is not a context: this will just be printed.
            elif type(action) == str:
                self.print(action)
                continue

# A "dict short version": we have to guess the action.
            elif type(action) == dict:
                action_args   = []
                action_kwargs = action

                if VAR_TITLE in action:
                    action = TITLE

                elif VAR_STEP_INFO in action:
                    action = STEP

                elif VAR_CONTEXT in action:
                    action = PROBLEM

                else:
                    raise ValueError(
                          "impossible to guess the action with the dict:\n"
                        + repr(action)
                    )

# Actions given with args.
            else:
                action_args   = []
                action_kwargs = {}

                action, *extras = action

# ''extras'' is just on dict.
                if (
                    len(extras) == 1
                    and
                    type(extras[0]) == dict
                ):
                    action_kwargs = extras[0]

# ''extras'' is a list of args.
                else:
                    action_args = extras

# End of the so clever analysis :-) .
#
# We can call the good action with the good args.
            getattr(self, action)(*action_args, **action_kwargs)

# Default "for all" normal context.
        self.forall()
        self.style()
