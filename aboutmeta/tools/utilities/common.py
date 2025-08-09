#!/usr/bin/env python3

# Rich colors: python -m rich.color

from typing import Any

import                   logging
from rich.logging import RichHandler
from rich.console import Console

from pathlib     import Path
import                  re

import           tomli
from yaml import safe_load

from black import (
    format_file_in_place,
    FileMode,
    WriteBack
)


# --------------- #
# -- CONSTANTS -- #
# --------------- #

INIT_FILE    = "__init__.py"
INIT_CONTENT = "#!/usr/bin/env python3\n"


TAG_STATUS = "status"
TAG_OK     = "ok"


TAG_CRITICAL = "critical"
TAG_WARNING  = "warning"


# ------------------------------- #
# -- LOGGING "DYNAMIC" CONFIG. -- #
# ------------------------------- #

LOG_FILE = "tools.log"


###
# XXXXXXX
###
class FileFormatter(logging.Formatter):
    def format(self, record):
        original_message = record.getMessage()
        cleaned_message  = re.sub(r'\[.*?\]', '', original_message)

        record.msg        = cleaned_message
        formatted_message = super().format(record)
        record.msg        = original_message

        return formatted_message


###
# XXXXXXX
###
class ColorFilter(logging.Filter):
    def filter(self, record):
        original_levelname = record.levelname

        if record.levelno >= logging.CRITICAL:
            record.msg = f"[black on orange1]{record.msg}[/black on orange1]"

        elif record.levelno >= logging.ERROR:
            record.msg = f"[bright_red]{record.msg}[/bright_red]"

        elif record.levelno >= logging.WARNING:
            record.msg = f"[dark_goldenrod]{record.msg}[/dark_goldenrod]"

        return True


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
# color is used
    console = Console(
        stderr=True,
        color_system=None if no_color else "auto"
    )

# File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="a"
    )
    file_handler.setLevel(logging.ERROR)

    file_formatter = FileFormatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
    file_handler.setFormatter(file_formatter)

# Terminal handler
    term_handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        markup=True
    )
    term_handler.setLevel(logging.INFO)

# Apply global config
    logging.basicConfig(
# Resetting configurations
        force=True,
        level=logging.INFO,
        handlers=[term_handler, file_handler],
    )

# Appliquer le filtre UNIQUEMENT au gestionnaire de la console
    term_handler.addFilter(ColorFilter())



###
# XXXXXXX
###
setup_logging()


###
# XXXXXXX
###
def log_title(
    title,
    desc,
):
    return f"{title.upper()} - {desc}"


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


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    setup_logging()
    logging.info("One information.")
    # logging.debug("Debugging?")
    logging.warning("One warning!")
    logging.error("An error!")
    logging.critical("A critical error!")
