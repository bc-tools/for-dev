#!/usr/bin/env python3

###
# This module implements the [C]-ommand [L]-ine [I]-nterface of \thisproj.
###


from typing import Tuple

import                        typer
from typing_extensions import Annotated

from .__init__ import __version__
from .build    import Builder, Path


# --------- #
# -- CLI -- #
# --------- #

CLI = typer.Typer()


###
# prototype::
#     version : set to ''True'', this \arg asks to print the current
#               \nb_ver of \thisproj.
#     src     : the \src \dir path with the MD chunks to be merged.
#     dest    : the final MD path of the file to build.
#     erase   : set to ''True'', this \arg allows to erase an existing
#               final file to build a new version of it.
#
#     :action: :see: build.Builder
###
@CLI.command(
    help             = "Merging MD chunks into a single MD file.",
    context_settings = dict(
        help_option_names = ["--help", "-h"]
    ),
)
def _CLI(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help = "Print the current number version.",
        ),
    ] = False,
    #
    src: Annotated[
        Path,
        typer.Argument(
            help = "Path of the source directory with the MD "
                   "chunks to be merged, followed by the path "
                   "of the final MD file to build."
        ),
    ] = None,
    #
    dest: Annotated[
        Path,
        typer.Argument(
            help = "Path of the source directory with the MD "
                   "chunks to be merged, followed by the path "
                   "of the final MD file to build."
        ),
    ] = None,
    #
    erase: Annotated[
        bool,
        typer.Option(
            "--erase",
            "-e",
            help = "Erase an existing final MD file before "
                   "building the new one.",
        ),
    ] = False,
) -> None:
# Number version?
    if version:
        if not src is None or erase:
            raise ValueError(
                f"''--version'' or ''-v'' must be used alone."
            )

        print(f"multimd {__version__}")
        exit(0)

# Nothing to do.
    if src is None or dest is None:
        raise ValueError("missing source and/or destination.")

# Relative to absolute?
    cwd = Path.cwd()

    src_dest     = [src, dest]
    dest_message = src_dest[1]

    for i, p in enumerate(src_dest):
        if not p.is_absolute():
            src_dest[i] = cwd / p

# Let's call our worker.
    Builder(
        erase = erase,
        *src_dest
    ).build()

# Let's talk to the user.
    if Path(dest_message).is_absolute():
        message = f"""
Successfully built file.
  + Full path given:
    {dest_message}
        """

    else:
        message = f"""
Successfully built file.
  + Path given:
    {dest_message}
  + Full path used:
    {src_dest[1]}
        """

    print(message.strip())
