#!/usr/bin/env python3

###
# This module implements the [C]-ommand [L]-ine [I]-nterface
# of \thisproj.
###


from typing import (
    Any,
    List,
)

import                        typer
from typing_extensions import Annotated
from rich.console      import Console

from copy    import deepcopy
from pathlib import Path

from box import BoxKeyError
from yaml    import dump as yaml_dump

from aboutmeta.amdata import (
    AMData,
    LOG_FILE
)

from aboutmeta.__init__     import __version__
from aboutmeta.data.helpers import HELPERS
from aboutmeta.data.specs   import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

NO_COLOR = False

# See: https://rich.readthedocs.io/en/stable/appendix/colors.html

FMT_INFO      = "[bold green]"
FMT_INFO_XTRA = "[yellow]"

FMT_IMPORTANT      = "[bold orange3]"
FMT_IMPORTANT_XTRA = "[tan]"

FMT_SUCCESS      = "[bold blue]"
FMT_SUCCESS_XTRA = "[cyan]"

FMT_ERROR      = "[bold bright_red]"
FMT_ERROR_XTRA = "[red3]"


TAB_1 = "  "
TAB_2 = TAB_1*2
TAB_3 = TAB_1*2

ITEM_1 = f"{TAB_1}+ "
ITEM_2 = f"{TAB_2}- "
ITEM_3 = f"{TAB_3}* "


TAG_WHAT = "what"

TAG_NO   = "no"
TAGS_YES = [
    TAG_YES:= "yes",
    TAG_YES[0]
]

TAG_ABORT = "x"

TXT_SPECIAL_KEY = "Special keys"
_TAB_SPE_KEY    = " "*(4 + len(TXT_SPECIAL_KEY))

TXT_HOW_ABORT = (
    f'"{TAG_ABORT.upper()}" / "{TAG_ABORT}" to go out of '
     'the parent block'
)

TXT_CHOICES_ABORT = (
     '"SPACE(S)" to move on to the next step'
     "\n"
    f"{_TAB_SPE_KEY}{TXT_HOW_ABORT}"

)
TXT_CHOICES_YES_NO = (
    f'"[{TAG_YES[0]}]{TAG_YES[1:]}" to accept'
     "\n"
    f"{_TAB_SPE_KEY}{TXT_HOW_ABORT}"
)


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# prototype::
#     nb_line : the number of lines to removed.
#
#     :action: the last ''nb_line'' terminal lines is removed.
###
def remove_lastline(
    nb_line: int = 1
) -> None:
    for _ in range(nb_line):
        print("\033[F\033[K", end = '')

    print()


###
# prototype::
#     lines : a list of lines of text that can be formatted using
#             \rich markup \lang.
#
#     :action: printing of text lines formatted as expected.
###
def fmt_print_lines(lines: List[str]) -> None:
    for l in lines:
        fmt_print(l)


###
# prototype::
#     action_done  : text about the process activated.
#     initial_args : the list of initial \args used when calling
#                    the \cli \cmd.
#
#     :action: print the action done, and its initial \args.
###
def start_communication(
    action_done : str,
    initial_args: List[str]
) -> None:
    infos  = [f"{FMT_INFO}{action_done}"]
    infos += [
        f"{FMT_INFO_XTRA}{ITEM_1}{arg}: {val}"
        for arg, val in initial_args.items()
    ]
    infos += [""]

    fmt_print_lines(infos)


###
# prototype::
#     message : explanations about the action in progress.
#     choices : text explaining the user's actions available.
#
#     :return: the user's response is analyzed, and if it's equal
#              to ''x'' or ''X'', it becomes the empty string (this
#              indicates to stop the data creation in progress).
###
def get_answer(
    message  : str,
    choices  : str,
) -> str:
    answer = typer.prompt(
        f"> {message}\n"
        f"  \033[33m{TXT_SPECIAL_KEY}: {choices}\n"
    )
    answer = answer.strip()

    return answer


###
# prototype::
#     answer  : the user's answer (that can be an information that
#               will be processed later by other functions).
#     relpath : the list of parent \yaml keys.
#
#     :return: ''False'' if the process should not be stopped, and
#              ''True'' if it should.
#              In the latter case, the function informs the user of
#              the imminent interruption of the process.
###
def must_abort(
    answer : str,
    relpath: List[str]
 ) -> bool:
    if answer != TAG_ABORT:
        return False

    remove_lastline(4)

    if relpath:
        relpath = '.'.join(relpath)

        xtra_1 = 'intermediate'
        xtra_2 = (
            f"{FMT_IMPORTANT_XTRA}We were working on ''{relpath}''."
        )

    else:
        xtra_1 = 'main'


    lines = [
        f"{FMT_IMPORTANT}End of {xtra_1} processing!"
    ]

    if relpath:
        lines.append(xtra_2)

    lines.append('')

    fmt_print_lines(lines)

    return True


# ---------------- #
# -- CLI - MAIN -- #
# ---------------- #

CLI = typer.Typer(
    context_settings = {
        "help_option_names": ["-h", "--help"]
    }
)


fmt_print = Console(no_color = False).print

###
# prototype::
#     no_color : :see: data.logconf.setup_logging
###
@CLI.callback()
def main(
    no_color: Annotated[
        bool,
        typer.Option(
            "--no-color",
            "-nc",
            help = "Disable highlighting messages with colors.",
        ),
    ] = False,
):
    global fmt_print, NO_COLOR

    NO_COLOR  = no_color
    fmt_print = Console(no_color = NO_COLOR).print


# ------------------ #
# -- CLI - CREATE -- #
# ------------------ #

###
# prototype::
#     file     : the path::''about.yaml'' file to be created from
#                scratch.
#     validate : validations are done interactively.
#     erase    : set to ''True'', this \arg allows to erase an
#                existing path::''about.yaml'' file.
#
#     :action: creation of the path::''about.yaml'' file containing
#              all mandatory data and all optional data chosen by
#              the user.
###
@CLI.command()
def create(
    file: Annotated[
        Path,
        typer.Argument(
            help = "Path of the ''about.yaml'' file."
        ),
    ],
    validate: Annotated[
        bool,
        typer.Option(
            "--validate",
            "-v",
            help = (
                "Validate parsed data (that have a validator). "
                "\nWARNING! Some validators require an Internet connection."
            ),
        ),
    ] = False,
    erase: Annotated[
        bool,
        typer.Option(
            "--erase",
            "-e",
            help = "Erase an existing ''about.yaml'' file.",
        ),
    ] = False,
):
    """
    Step-by-step creation of an ''about.yaml'' file.
    """
    initial_args = dict(**locals())

# Start of communication.
    start_communication(
        action_done = (
            "Step-by-step creation of your ''about.yaml'' file."
        ),
        initial_args = initial_args,
    )

    fmt_print_lines([
        f"{FMT_INFO}NOTE: we give virtual pointed paths "
         "of blocks and keys.",
        ''
    ])

# Validation of the file.
    yaml_file = Path(file)

    if not yaml_file.suffix == ".yaml":
        ext = yaml_file.suffix

        if ext:
            ext = ext[1:]

        xtra = f", and not ''{ext}''" if ext else ""


        fmt_print_lines([
            f"{FMT_ERROR}File must use the ''yaml'' extension{xtra}. ",
            f"{FMT_ERROR_XTRA}See {yaml_file}",
        ])

        exit(1)

    if (
        not erase
        and
        yaml_file.is_file()
    ):
        fmt_print_lines([
            f"{FMT_ERROR}File cannot be overwritten.",
            f"{FMT_ERROR_XTRA}See {yaml_file}",
        ])

        exit(1)

# We can work recursively.
    content = recu_create(deepcopy(SPECS))

# End of communication.
    if not content:
        xtra = "modified" if yaml_file.is_file() else "created"

        fmt_print_lines([
            f"{FMT_ERROR}Un{xtra} file (no content created).",
            f"{FMT_ERROR_XTRA}See {file}"
        ])

    else:
        yaml_file.touch()

        with yaml_file.open(mode = 'w') as f:
            yaml_dump(content, f)

        fmt_print_lines([
            f"{FMT_SUCCESS}File created with the expected data.",
            f"{FMT_SUCCESS_XTRA}See {file}"
        ])


###
# prototype::
#     loc_specs : "local" \specs corresponding to the data being
#                 analyzed.
#     relpath   : :see: must_abort
#
#     :return: the dict build with data given by the user.
###
def recu_create(
    loc_specs: dict,
    relpath  : List[str] = []
) -> dict:
    content = dict()
    amdata  = AMData()

# Alternatives?
    all_alts = loc_specs[TAG_SPECS_ALT_ALL]
    del loc_specs[TAG_SPECS_ALT_ALL]

    if all_alts:
        alt_tuples = loc_specs[TAG_SPECS_ALT_TUPLES]
        del loc_specs[TAG_SPECS_ALT_TUPLES]


# YAML keys.
    for key, about in loc_specs.items():
# TODO!
        if key in all_alts:
            fmt_print(f"{FMT_ERROR}{key} not managed!")
            continue

# About the key.
        is_required = about[TAG_SPECS_REQUIRED]
        yaml_type   = about[TAG_SPECS_TYPE]

# Helper for the key.
        keypath     = relpath + [key]
        str_keypath = '.'.join(keypath)

        helper = HELPERS.get(str_keypath, "")

        fmt_print(f"{FMT_INFO_XTRA}[bold]{str_keypath}  ")

        if helper:
            fmt_print(f"{FMT_INFO_XTRA}{helper}")

# Recursive creations for a block.
        if yaml_type == TAG_SPECS_BLOCK:
            answer = get_answer(
                message   = "Add this block.",
                choices   = TXT_CHOICES_YES_NO,
            ).lower()

            if must_abort(
                answer  = answer,
                relpath = relpath
            ):
                return content

            remove_lastline(4)

            if answer in TAGS_YES:
                sub_content = recu_create(
                    loc_specs = loc_specs[key][TAG_SPECS_CONTENT],
                    relpath   = keypath
                )

                if sub_content:
                    content[key] = sub_content

            continue

# Do we have to create new data.
        is_list_of = about[TAG_SPECS_LIST_OF]

        xtra = "a list of " if is_list_of else "one"

        answer = get_answer(
            message = f"Creation of {xtra} data.",
            choices = TXT_CHOICES_ABORT
        )

# Go out of this block?
        if must_abort(
            answer  = answer,
            relpath = relpath
        ):
            return content

# Let the user works.
        parser     = getattr(
            amdata._parsers,
            about[TAG_SPECS_PARSER]
        )

        try:
            data = process_data(
                data       = answer,
                is_list_of = is_list_of,
                parser     = parser,
            )

        except ValueError as e:
            fmt_print_lines([
                '',
                f"{FMT_ERROR}Data creation has raised an error. See below.",
            ])

            exit(1)

        content[key] = data

# Processing the user's information.
        fmt_print()

# Nothing left to do.
    return content


###
# prototype::
#     x : y
#
#     :return: z
###
def process_data(
    data      : str,
    is_list_of: bool,
    parser    : Any,
) -> str:
    if is_list_of:
        return process_data_list(
            data   = data,
            parser = parser
        )

    return process_data_single(
        data   = data,
        parser = parser
    )


###
# prototype::
#     x : y
#
#     :return: z
###
def process_data_single(
    data  : str,
    parser: Any,
) -> str:
    return f"{parser.__name__}"

###
# prototype::
#     x : y
#
#     :return: z
###
def process_data_list(
    data  : str,
    parser: Any,
) -> List[str]:
    return f"{parser.__name__}"


# -------------------- #
# -- CLI - VALIDATE -- #
# -------------------- #

###
# prototype::
#     file      : :see: data.pre_amdata.PreAMData.build
#     what      : :see: data.pre_amdata.PreAMData.validate
#     erase_log : :see: data.pre_amdata.PreAMData.validate
#
#     :action: :see: data.pre_amdata.PreAMData.validate
###
@CLI.command()
def validate(
    file: Annotated[
        Path,
        typer.Argument(
            help = "Path of the ''about.yaml'' file."
        ),
    ],
    what: Annotated[
        str,
        typer.Option(
            "--what",
            "-w",
            help = (
                "The pointed virtual path of a specific key to "
                "analyze (the key can have a block value)."
            ),
        ),
    ] = None,
    erase_log: Annotated[
        bool,
        typer.Option(
            "--erase",
            "-e",
            help = "Erase the log file.",
        ),
    ] = False,
):
    """
    Validating data from the ''about.yaml'' file: the validation
    process is detailed in the terminal, but only errors are
    recorded in the log file.
    """
    global NO_COLOR

    initial_args = dict(**locals())

    if initial_args[TAG_WHAT] is None:
        initial_args[TAG_WHAT] = "all data"

# Start of communication.
    start_communication(
        action_done = "Starting validation.",
        initial_args = initial_args,
    )

# Let ''AMData'' do its job.
    amdata = AMData()

    try:
        amdata.build(yaml_file = file)

    except FileNotFoundError as e:
        fmt_print_lines([
            f"{FMT_ERROR}No such fle:",
            f"{FMT_ERROR_XTRA}{file}",
        ])

        exit(1)

    try:
        nb_errors = amdata.validate(
            what      = what,
            erase_log = erase_log,
            no_color  = NO_COLOR,
        )

    except BoxKeyError as e:
        fmt_print_lines([
            f"{FMT_ERROR}Illegal pointed virtual path ''{what}''.",
        ])

        exit(1)

# DEBUG - START
    # nb_errors = 0
    # nb_errors = 1
# DEBUG - END

# End of communication.
    if not amdata.at_least_one_validation:
        infos = [
            f"{FMT_SUCCESS}NO DATA TO VALIDATE!",
        ]

    elif nb_errors == 0:
        infos = [
            '',
            f"{FMT_SUCCESS}DATA VALIDATED!",
        ]

        infos += [
            f"{FMT_SUCCESS_XTRA}{ITEM_1}{arg}: {val}"
            for arg, val in initial_args.items()
        ]

    else:
        plurial = "" if nb_errors == 1 else "S"

        infos = [
            '',
            f"{FMT_ERROR}{nb_errors} ERROR{plurial} FOUND.",
            f"{FMT_ERROR_XTRA}See: {LOG_FILE}",
        ]

    fmt_print_lines(infos)
