#!/usr/bin/env python3

# from pprint import pprint

from typing import Any

import                   logging
from rich.logging import RichHandler
from rich.console import Console

from pathlib     import Path
import                  re

import           tomli
from yaml import safe_load


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# TAB_1 = ' '*2
# TAB_2 = TAB_1*2
# TAB_3 = TAB_1*3

# ITEM_1 = '+'
# ITEM_2 = f'{TAB_1}*'
# ITEM_3 = f'{TAB_2}-'
# ITEM_4 = f'{TAB_3}-->'


INIT_FILE    = "__init__.py"
INIT_CONTENT = "#!/usr/bin/env python3\n"


TAG_STATUS = "status"
TAG_OK     = "ok"


# ------------------------------- #
# -- LOGGING "DYNAMIC" CONFIG. -- #
# ------------------------------- #

LOG_FILE = "tools.log"


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


setup_logging()


def log_title(
    title,
    desc,
):
    return f"{{{title.upper()}}}  {desc}"


# ----------- #
# -- PATHS -- #
# ----------- #

def get_folders(
    this_dir,
    contrib_dir,
    context,
    nbtest,
    subfolder = "code",
):
    projdir  = this_dir.parent.parent
    projname = projdir.name

    contribdir = projdir / "contrib" / contrib_dir / subfolder
    statusdir  = contribdir.parent / "status"
    srcdir     = projdir / "src" / projname / context
    testsdir   = projdir / "tests" / f"{nbtest}-{context}"

    return (
        projdir,
        projname,
        contribdir,
        statusdir,
        srcdir,
        testsdir
    )


# WARNING!
# "No status" ==> "No parser to add"
def get_accepted_paths(
    contribdir,
    statusdir,
    subfolder = "",
    ext       = 'py',
):
    files = []

    if subfolder:
        subfolder += "/"

    for yaml_file in statusdir.glob(
        f"{subfolder}*.yaml"
    ):
        statusdata = safe_load(yaml_file.read_text())

        if statusdata[TAG_STATUS] != TAG_OK:
            continue

        file = contribdir / f"{yaml_file.stem}.{ext}"

        if not file.is_file():
            raise IOError(f"missing file:\n{file}")

        files.append(file)

    files.sort()

    return files
