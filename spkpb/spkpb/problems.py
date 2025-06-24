#!/usr/bin/env python3

###
# This module defines the class ''Problems'' to indicate warnings,
# "criticals" and errors.
###


from collections import defaultdict

from natsort import natsorted

from .speaker import *


# ------------------------ #
# -- PROBLEMS DECORATOR -- #
# ------------------------ #

###
# This decorator simplifies the managment of the new warnings, criticals
# and errors.
###
def problems_deco(method):

###
# prototype::
#     what  : any object with a string representation indicating clearly
#             what is causing the problem.
#     info  : the info explaining the problem.
#     level : the level of the step indicating the problem.
#           @ :in: 0..3
###
    def similar(
        self,
        what : Any,
        info : str,
        level: int = 0
    ) -> None:
        kind = method.__name__.replace('new_', '')

        nb_kind = f'nb_{kind}s'

        lastnb = getattr(self, nb_kind)
        setattr(self, nb_kind, lastnb + 1)

        self._new_pb(
            what    = what,
            context = globals()[f'CONTEXT_{kind.upper()}'],
            info    = info,
            level   = level
        )

    return similar


# -------------- #
# -- PROBLEMS -- #
# -------------- #

###
# This class is used to store ¨infos about errors and warnings emitted
# during all the process.
###
class Problems:
    PB_INFO_TAG: str = 'info'
    PB_ID_TAG  : str = 'pbid'

###
# prototype::
#     speaker : an instance of ''speaker.allinone.Speaker'' that is used
#               to communicate small ¨infos.
###
    def __init__(
        self,
        speaker: Speaker,
    ) -> None:
        self.speaker = speaker

        self.reset()


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
# Reset the numbering of steps.
        self.speaker.reset()

# ---------
# WARNING !
# ---------
#
# We use the ordered feature of dict such as to treat warnings, criticals
# and errors in this order when printing the summaries.
        self.problems_found : dict = {
            CONTEXT_WARNING : defaultdict(list), # Before ERROR and CRITICAL!
            CONTEXT_CRITICAL: defaultdict(list), # Before ERROR!
            CONTEXT_ERROR   : defaultdict(list),
        }

        self.nb_warnings  = 0
        self.nb_criticals = 0
        self.nb_errors    = 0

        self._pb_id = 0


###
# prototype::
#     :return: ''True'' if at least one warning has been found and
#              ''False` otherwise.
###
    @property
    def warningfound(self) -> bool:
        return self.nb_warnings != 0


###
# prototype::
#     :return: ''True'' if at least one "critical" has been found and
#              ''False` otherwise.
###
    @property
    def criticalfound(self) -> bool:
        return self.nb_warnings != 0


###
# prototype::
#     :return: ''True'' if at least one error has been found and
#              ''False` otherwise.
###
    @property
    def errorfound(self) -> bool:
        return self.nb_errors != 0


###
# prototype::
#     :return: ''True'' if at least on error or one warning has been found and
#              ''False` otherwise.
###
    @property
    def pbfound(self) -> bool:
        return (
            self.warningfound
            or
            self.criticalfound
            or
            self.errorfound
        )


###
# prototype::
#     :return: ''True'' if there are several warnings and
#              ''False'' otherwise.
###
    @property
    def several_warnings(self) -> bool:
        return self.nb_warnings > 1


###
# prototype::
#     :return: ''True'' if there are several "criticals" and
#              ''False'' otherwise.
###
    @property
    def several_criticals(self) -> bool:
        return self.nb_criticals > 1


###
# prototype::
#     :return: ''True'' if there are several erros and
#              ''False'' otherwise.
###
    @property
    def several_errors(self) -> bool:
        return self.nb_errors > 1


###
# prototype::
#     what  : any object with a string representation indicating clearly
#             what is causing the warning.
#     info  : the info explaining the warning.
#     level : the level of the step indicating the problem.
#           @ :in: 0..3
###
    @problems_deco
    def new_warning(
        self,
        what : Any,
        info : str,
        level: int = 0
    ) -> None:
        ...


###
# prototype::
#     what  : any object with a string representation indicating clearly
#             what is causing the "critical" which is a dangerous warning.
#     info  : the info explaining the "critical".
#     level : the level of the step indicating the problem.
#           @ :in: 0..3
###
    @problems_deco
    def new_critical(
        self,
        what : Any,
        info : str,
        level: int = 0
    ) -> None:
        ...


###
# prototype::
#     what  : any object with a string representation indicating clearly
#             what is causing the error.
#     info  : the info explaining the error.
#     level : the level of the step indicating the problem.
#           @ :in: 0..3
###
    @problems_deco
    def new_error(
        self,
        what : Any,
        info : str,
        level: int = 0
    ) -> None:
        ...


###
# prototype::
#     what    : any object with a string representation indicating clearly
#               what is causing the problem.
#     context : the kind of problem.
#             @ :in: [speaker.spk_interface.CONTEXT_ERROR,
#                     speaker.spk_interface.CONTEXT_WARNING]
#     info    : the info explaining the problem.
#     level   : the level of the step indicating the problem.
#             @ :in: 0..3
###
    def _new_pb(
        self,
        what   : Any,
        context: str,
        info   : str,
        level  : int = 2
    ) -> None:
# Let's store the problems internally.
        self._pb_id += 1
        self.problems_found[context][str(what)].append({
            self.PB_ID_TAG  : self._pb_id,
            self.PB_INFO_TAG: info,
        })

# Let's talk to the world...
        self.speaker.problem(
            context = context,
            info    = info,
            level   = level,
            pb_id   = self._pb_id
        )


###
# This method prints the summaries for the terminal and the log file.
###
    def resume(self) -> None:
# Silent must be switch off here...
        onlyresume_user         = self.speaker.onlyresume
        self.speaker.onlyresume = False

# Let's talk...
        showref = add_NL = not onlyresume_user

        for context, pbs in self.problems_found.items():
            if not pbs:
                continue

# Header
            total_nb_pbs = getattr(self, f'nb_{context.lower()}s')

            plurial = "S" if total_nb_pbs > 1 else ""

            if add_NL:
                self.speaker.NL()

            if onlyresume_user:
                add_NL = True

            self.speaker.recipe(
                context,
                {VAR_TITLE:
                    f'{total_nb_pbs} {context.upper()}{plurial} FOUND',
                 VAR_LEVEL  : 2,
                 VAR_WITH_NL: False},
            )

# Verbose in the terminal?
            if not onlyresume_user:
                self.speaker.recipe(
                    context,
                    FORTERM,
                        NL,
                        'Look at the log file or above for details.',
                )

# The problems (cardinality + refs).
            for what in natsorted([
                str(p) for p in pbs
            ]):
                if onlyresume_user:
                    verb_in = [FORTERM, FORLOG]

                else:
                    verb_in = [FORLOG]

                    self._resume_one_pb_short(
                        what    = what,
                        whatpbs = pbs[what],
                        context = context,
                    )

                self._resume_one_pb_verbose(
                    what    = what,
                    whatpbs = pbs[what],
                    context = context,
                    verb_in = verb_in,
                    showref = showref,
                )

# Let's go back to the silent user's choice.
        self.speaker.onlyresume = onlyresume_user

###
# prototype::
#     what    : any object with a string representation indicating clearly
#               what is causing the problem.
#     whatpbs : the list of problems for the same ''what''.
#     context : the kind of problem.
#             @ :in: [speaker.spk_interface.CONTEXT_ERROR,
#                     speaker.spk_interface.CONTEXT_WARNING]
###
    def _resume_one_pb_short(
        self,
        what   : str,
        whatpbs: List[dict],
        context: str,
    ):
        pbs_ids = [
            onepb[self.PB_ID_TAG]
            for onepb in whatpbs
        ]

        nb_pbs = len(whatpbs)

        plurial = "s" if nb_pbs > 1 else ""

        self.speaker.recipe(
            FORTERM,
                context,
                NL,
                {VAR_STEP_INFO: what,
                VAR_LEVEL    : 1},
        )

        self.speaker.recipe(
            FORTERM,
                context,
                    {VAR_STEP_INFO: (
                        f'{nb_pbs} {context}{plurial}.'
                        '\n'
                        f'See #.: {pbs_ids}.'),
                    VAR_LEVEL: 2},
        )


###
# prototype::
#     what    : any object with a string representation indicating clearly
#               what is causing the problem.
#     whatpbs : the list of problems for the same ''what''.
#     context : the kind of problem.
#             @ :in: [speaker.spk_interface.CONTEXT_ERROR,
#                     speaker.spk_interface.CONTEXT_WARNING]
#     verb_in : the list of outputs where to be verbose.
#     showref : ''True'' asks to show the references (for a none silent mode)
#               contrary to ''False''.
###
    def _resume_one_pb_verbose(
        self,
        what   : str,
        whatpbs: List[dict],
        context: str,
        verb_in: List[str],
        showref: bool,
    ):
        for output in verb_in:
            self.speaker.recipe(
                output,
                    context,
                    NL,
                    {VAR_STEP_INFO: what,
                     VAR_LEVEL    : 1},
            )

            for onepb in whatpbs:
                info = onepb[self.PB_INFO_TAG]

                if showref:
                    pbid = onepb[self.PB_ID_TAG]

                    message = f'See [ #.{pbid} ] : {info}'

                else:
                    message = info[0].upper() + info[1:]

                self.speaker.recipe(
                    output,
                        context,
                        {VAR_STEP_INFO: message,
                         VAR_LEVEL    : 2},
                )
