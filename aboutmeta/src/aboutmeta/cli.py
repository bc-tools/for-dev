#!/usr/bin/env python3

###
# This module implements the [C]-ommand [L]-ine [I]-nterface
# of \thisproj.
###


from typing import (
    Dict,
    List,
)

import                        typer
from typing_extensions import Annotated
from rich              import print

from copy    import deepcopy
from pathlib import Path
from yaml    import dump as yaml_dump

from box import BoxKeyError

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

TAG_ABORT = "x"
TAG_NO    = "no"

TAGS_YES = [
    TAG_YES:= "yes",
    TAG_YES[0]
]


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# prototype::
#     lines : a list of lines of text that may contain formatting
#             directives \rich.
#
#     :action: printing of text lines formatted as expected.
###
def print_lines(lines: List[str]) -> None:
    for l in lines:
        print(l)


###
# prototype::
#     action_done  : text about the process activated.
#     initial_args : the list of initial \args.
#
#     :action: print the initial \args about the process done.
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

    print_lines(infos)


# ---------------- #
# -- CLI - INIT -- #
# ---------------- #

CLI = typer.Typer(
    context_settings = {
        "help_option_names": ["-h", "--help"]
    }
)


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

# Validation of the file.
    yaml_file = Path(file)

    if not yaml_file.suffix == ".yaml":
        ext = yaml_file.suffix

        if ext:
            ext = ext[1:]

        xtra = f", and not ''{ext}''" if ext else ""


        print_lines([
            f"{FMT_ERROR}File must use the ''yaml'' extension{xtra}. ",
            f"{FMT_ERROR_XTRA}See {yaml_file}",
        ])

        exit(1)

    if (
        not erase
        and
        yaml_file.is_file()
    ):
        print_lines([
            f"{FMT_ERROR}File cannot be overwritten.",
            f"{FMT_ERROR_XTRA}See {yaml_file}",
        ])

        exit(1)

# We can work recursively.
    content = recu_create(deepcopy(SPECS))

# End of communication.
    if not content:
        xtra = "modified" if yaml_file.is_file() else "created"

        print_lines([
            f"{FMT_IMPORTANT}Un{xtra} file (no content).",
            f"{FMT_IMPORTANT_XTRA}See {file}"
        ])

    else:
        yaml_file.touch()

        with yaml_file.open(mode = 'w') as f:
            yaml_dump(content, f)

        print_lines([
            f"{FMT_SUCCESS}File created with the expected data.",
            f"{FMT_SUCCESS_XTRA}See {file}"
        ])


###
# prototype::
#     loc_specs : "local" \specs corresponding to the data analyzed.
#     relpath   : xxxx
#
#     :return: xxxxx
###
def recu_create(
    loc_specs: dict,
    relpath  : List[str] = []
) -> List[str]:
    content = dict()
    content = {'TO': "DO"}

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
            print(f"{FMT_ERROR}{key} not managed!")
            continue

# About the key.
        is_required = about[TAG_SPECS_REQUIRED]
        yaml_type   = about[TAG_SPECS_TYPE]

# Helper for the key.
        keypath     = relpath + [key]
        str_keypath = '.'.join(keypath)

        helper = HELPERS.get(str_keypath, "")

        print(f"{FMT_INFO_XTRA}[bold]{str_keypath}  ", end = "")
        print(f"[white](virtual pointed path given)")

        if helper:
            print(f"{FMT_INFO_XTRA}{helper}")

# Recursive creations for a block.
        if yaml_type == TAG_SPECS_BLOCK:
            if new_data(
                message   = "Add this block",
                choices   = "[y]es / [n]o",
                can_abort = False
            ).lower() in TAGS_YES:
                sub_content = recu_create(
                    loc_specs = loc_specs[key][TAG_SPECS_CONTENT],
                    relpath   = keypath
                )

                if sub_content:
                    content[key] = sub_content

            continue

# Data to add.
        parser = about[TAG_SPECS_PARSER]

# Creation of a list of textual data.
        if about[TAG_SPECS_LIST_OF]:
            data = new_data(f"list")

# Creation of a single textual data.
        else:
            data = new_data(f"single")

        print()

# Nothing left to do.
    return content


###
# prototype::
#     message   : explanations about the answer expeceted.
#     choices   : text explaining the user's actions available.
#     can_abort : set to ''True'', this \arg alllows to use SPACE,
#                 x or X to abort the data process in progress.
#                 Normally, this \arg should be equal to ''False''
#                 if ''choice'' does not have its default \val.
#
#     :return: the user's response is analyzed, and if it's equal
#              to “x” or “X”, it becomes the empty string (this
#              indicates to stop the data creation in progress).
###
def new_data(
    message  : str,
    choices  : str = "SPACE, x or X to abort",
    can_abort: bool = True
) -> str:
    answer = typer.prompt(f"{TAB_1}> {message}  ( {choices} )")
    answer = answer.strip()

    if can_abort and answer.lower() == TAG_ABORT:
        answer = ""

    return answer


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
    initial_args = dict(**locals())

    if initial_args[TAG_WHAT] is None:
        initial_args[TAG_WHAT] = "all data"

# Start of communication.
    start_communication(
        action_done = "Starting validation.",
        initial_args = initial_args,
    )

# Let “AMData” do its job.
    amdata = AMData()

    try:
        amdata.build(yaml_file = file)

    except FileNotFoundError as e:
        print_lines([
            f"{FMT_ERROR}No such fle:",
            f"{FMT_ERROR_XTRA}{file}",
        ])

        exit(1)

    try:
        nb_errors = amdata.validate(
            what      = what,
            erase_log = erase_log
        )

    except BoxKeyError as e:
        print_lines([
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
            f"{FMT_ERROR}{nb_errors} ERROR{plurial} FOUND. "
             "Look at the log file:",
            f"{FMT_ERROR_XTRA}{LOG_FILE}",
        ]

    print_lines(infos)
