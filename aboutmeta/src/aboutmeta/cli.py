#!/usr/bin/env python3

###
# This module implements the [C]-ommand [L]-ine [I]-nterface of \thisproj.
###


from typing import Tuple

import                        typer
from typing_extensions import Annotated

from aboutmeta.__init__ import __version__
from aboutmeta.amdata   import AMData

from aboutmeta.data import helpers


# --------- #
# -- CLI -- #
# --------- #

CLI = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]}
)


@CLI.command()
def help(topic: str):
    """
 Affiche l'aide pour un sujet spécifique.
    """
    typer.echo(f"Aide sur le sujet : {topic}")


@CLI.command()
def compile(
    file: str = typer.Argument(..., help="Fichier à compiler."),
    optimize: bool = typer.Option(False, "--opt", "-o",
    help="Activer l'optimisation."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux.")
):
    """
    Compile un fichier source.
    """
    typer.echo(f"Compilation de : {file}")
    if optimize:
        typer.echo(" → Optimisation activée.")
    if verbose:
        typer.echo(" → Mode verbeux.")
