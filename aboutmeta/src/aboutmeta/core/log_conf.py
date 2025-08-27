#!/usr/bin/env python3

from typing import Any

import                   logging
from rich.logging import RichHandler
from rich.console import Console


# ------------------------------- #
# -- LOGGING "DYNAMIC" CONFIG. -- #
# ------------------------------- #

LOG_FILE = "aboutmeta.log"


###
# prototype::
#     no_color  : set to ''False'', the log information will be
#                 printed in color; otherwise, it will be printed
#                 in black and white.
#
#     :action: the function lives up to its name...
###
def setup_logging(no_color = False) -> None:
# Terminal handler
#
# ''color_system = "quto"'' detects whether the output is a real
# terminal. If not—such as when output is redirected via a pipe—no
# color is used.
    console = Console(
        stderr       = True,
        color_system = None if no_color else "auto"
    )

# ''markup = True'' allows to use the formatting markup language
# of rich.
    term_handler = RichHandler(
        console         = console,
        rich_tracebacks = True,
        markup          = True
    )
    term_handler.setLevel(logging.INFO)

# File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        mode = "a"
    )
    file_handler.setLevel(logging.ERROR)

    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
    file_handler.setFormatter(file_formatter)

# Apply global config
    logging.basicConfig(
# Resetting configurations
        force    = True,
# Lowest level for taking our levels into account.
        level    = logging.DEBUG,
        handlers = [
            term_handler,
            file_handler
        ],
    )
