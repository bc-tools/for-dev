#!/usr/bin/env python3

###
# This module implements the [C]-ommand [L]-ine [I]-nterface of ¨cofiup.
###


import click


# --------- #
# -- CLI -- #
# --------- #

###
# prototype::
#     message : this text is to indicate one error.
#
#     :action: an error message is printed, then the script exits
#              with a ''1'' error.
###
def _exit(message: str) -> None:
    print(
f"""
Try 'cofiup --help' for help.

Error: {message}
""".strip()
    )

    exit(1)


###
# prototype::
###
def cfp_CLI(
) -> None:
    """
    ???
    """
    ...
