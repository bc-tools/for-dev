#!/usr/bin/env python3

from typing import Any

import                   logging
from rich.logging import RichHandler
from rich.console import Console


# ------------------------------- #
# -- LOGGING 'DYNAMIC' CONFIG. -- #
# ------------------------------- #

LOG_FILE = 'aboutmeta.log'


###
# prototype::
#     no_color: set to ''False'', the log information will be
#         printed in color; otherwise, it will be printed in black
#         and white.
#
#     :action: the function lives up to its name...
#
#     :return: a ''Console'' instance. This is used to record an
#         SVG screenshot of a colorful session.
###
def setup_logging(no_color: bool = False) -> Console:
# Terminal handler
#
# ''color_system = 'auto''' detects whether the output is a real
# terminal. If not—such as when output is redirected via a pipe—no
# color is used.
    console = Console(
        record       = True,
        stderr       = True,
        color_system = None if no_color else 'auto',
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
        mode = 'a'
    )
    file_handler.setLevel(logging.ERROR)

    file_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s'
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

    return console


# ------------- #
# -- NO TEST -- #
# ------------- #

# We just check visually that settings are good.

if __name__ == '__main__':
    from pathlib import Path

    THIS_DIR       = Path(__file__).parent
    TOOLS_DATA_DIR = THIS_DIR

    while(TOOLS_DATA_DIR.name != 'for-dev'):
        TOOLS_DATA_DIR = TOOLS_DATA_DIR.parent

    TOOLS_DATA_DIR = TOOLS_DATA_DIR / 'aboutmeta' / 'tools' / 'data' / 'svg'

    for title, no_color in [
        ('COLORFUL', False),
        ('B & W'   , True),
    ]:
        print(f'-- {title} --')

        active_console = setup_logging(no_color)

        for level in [
            'info',
            'warning',
            'critical',
            'error',
        ]:
            getattr(
                logging,
                level
            )(f"Testing '{level}'")

        if title == 'COLORFUL':
            print('')
            print(f'Saving {title!r} SVG screenshot')

            active_console.save_svg(
                str(TOOLS_DATA_DIR  / f"term-output-{title}-LOGGING.svg")
            )
