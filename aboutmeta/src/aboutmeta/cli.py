#!/usr/bin/env python3

###
# This module implements the [C]-ommand [L]-ine [I]-nterface of \thisproj.
###


from typing import Tuple

import                        typer
from typing_extensions import Annotated

from pathlib import Path

from aboutmeta.amdata import AMData

from aboutmeta.__init__ import __version__
from aboutmeta.data     import helpers


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
    typer.echo(f"TODO")


# -------------------- #
# -- CLI - VALIDATE -- #
# -------------------- #

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
     Validating data from the ''about.yaml'' file: the validation process is detailed in the terminal, but only errors are recorded in the log file.
    """
    typer.echo(f"TODO")
