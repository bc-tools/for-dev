#!/usr/bin/env python3

###
# This module implements the [C]-ommand [L]-ine [I]-nterface of \thisproj.
###


from typing import Tuple

import                        typer
from typing_extensions import Annotated
from rich              import print

from pathlib import Path

from aboutmeta.amdata import (
    AMData,
    LOG_FILE
)

from aboutmeta.__init__ import __version__
from aboutmeta.data     import helpers


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# See: https://rich.readthedocs.io/en/stable/appendix/colors.html

FORMAT_INFO     = "[bold green]"
FORMAT_SUB_INFO = "[yellow]"

FORMAT_SUCCESS     = "[bold blue]"
FORMAT_SUB_SUCCESS = "[cyan]"

FORMAT_ERROR     = "[bold bright_red]"
FORMAT_SUB_ERROR = "[red3]"


# ---------------- #
# -- CLI - INIT -- #
# ---------------- #

CLI = typer.Typer(
    context_settings = {
        "help_option_names": ["-h", "--help"]
    }
)


# --------------- #
# -- CLI - NEW -- #
# --------------- #

@CLI.command()
def new():
    """
    Step-by-step creation of an ''about.yaml'' file.
    """
    print("[bold green]Step-by-step creation of your ''about.yaml'' file.")



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
            help = "The pointed path of a specific key to analyze (the key can have a block value).",
        ),
    ] = None,
    erase_log: Annotated[
        bool,
        typer.Option(
            "--erase",
            "-e",
            help = "Erasing the log file",
        ),
    ] = False,
):
    """
    Validating data from the ''about.yaml'' file: the validation
    process is detailed in the terminal, but only errors are
    recorded in the log file.
    """
    initial_args = dict(**locals())

# Starting communication.
    print(f"{FORMAT_INFO}Starting validation.")

    for arg, val in initial_args.items():
        print(f"{FORMAT_SUB_INFO}  + {arg}: {val}")

    print()

# Let ''AMData'' work.
    amdata = AMData()

    amdata.build(yaml_file = file)

    nb_errors = amdata.validate(
        what      = what,
        erase_log = erase_log
    )

# DEBUG - START
    # nb_errors = 0
    # nb_errors = 1
# DEBUG - END

# Closing communication.
    if nb_errors == 0:
        infos = [
            f"{FORMAT_SUCCESS}DATA VALIDATED!",
        ]

        infos += [
            f"{FORMAT_SUB_SUCCESS}  + {arg}: {val}"
            for arg, val in initial_args.items()
        ]

    else:
        plurial = "" if nb_errors == 1 else "S"

        infos = [
            f"{FORMAT_ERROR}{nb_errors} ERROR{plurial} FOUND. "
             "Look at the log file:",
            f"{FORMAT_SUB_ERROR}{LOG_FILE}",
        ]

    print()

    for i in infos:
        print(i)
