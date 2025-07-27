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

from pathlib import Path

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

FMT_ERROR      = "[bold bright_red]"
FMT_ERROR_XTRA = "[red3]"

FMT_SUCCESS      = "[bold blue]"
FMT_SUCCESS_XTRA = "[cyan]"

TAB_1 = "  "
TAB_2 = TAB_1*2
TAB_3 = TAB_1*2

ITEM_1 = f"{TAB_1}+ "
ITEM_2 = f"{TAB_2}- "
ITEM_3 = f"{TAB_3}* "

TAG_WHAT = "what"


# ----------- #
# -- TOOLS -- #
# ----------- #


# prototype::
#     lines : a list of lines of text that may contain formatting
#             directives \rich.
#
#     :action: printing of text lines formatted as expected.
def print_lines(lines: List[str]) -> None:
    for l in lines:
        print(l)


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
#     file  : the path::''about.yaml'' file to be created from
#             scratch.
#     erase : set to ''True'', this \arg allows to erase an
#             existing path::''about.yaml'' file.
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
# Start of communication.
    print_lines([
        f"{FMT_INFO}Step-by-step creation of "
         "your ''about.yaml'' file.",
        ""
    ])

# Validation of the file.
    yaml_file = Path(file)

    if not yaml_file.suffix == ".yaml":
        ext = yaml_file.suffix

        if ext:
            ext = ext[1:]

        xtra = f", and not ''{ext}''" if ext else ""


        print_lines([
            f"{FMT_ERROR}File must use the ''yaml'' extension{xtra}. ",
            f"{FMT_ERROR_XTRA}File proposed:",
            f"{FMT_ERROR_XTRA}{yaml_file}",
        ])

        exit(1)

    if (
        not erase
        and
        yaml_file.is_file()
    ):
        print_lines([
            f"{FMT_ERROR}File cannot be overwritten:",
            f"{FMT_ERROR_XTRA}{yaml_file}",
        ])

        exit(1)

# We can work recursively.
    yaml_file.touch()

    content = _recu_create(SPECS)

# End of communication.


###
# prototype::
#     XXXX
###
def _recu_create(
    loc_specs: Dict[str, str]
) -> List[str]:
    content = []

    print(loc_specs)
    exit()

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
    infos  = [f"{FMT_INFO}Starting validation."]
    infos += [
        f"{FMT_INFO_XTRA}{ITEM_1}{arg}: {val}"
        for arg, val in initial_args.items()
    ]
    infos += [""]

    print_lines(infos)

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
