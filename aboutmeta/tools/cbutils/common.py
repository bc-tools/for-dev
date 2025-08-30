#!/usr/bin/env python3

# Rich colors: python -m rich.color

from typing import Any

import                   logging
from rich.logging import RichHandler
from rich.console import Console

import              ast
from copy    import copy
from pathlib import Path
import              re

import           tomli
from yaml import safe_load

from black import (
    format_str,
    format_file_in_place,
    FileMode,
    WriteBack
)


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAG_INIT     = "__init__"
INIT_FILE    = f"{TAG_INIT}.py"
INIT_CONTENT = "#!/usr/bin/env python3\n"

TAG_CONSTANTS = "constants"
TAG_SIGNS     = "signatures"
TAG_SPECS     = "specs"
TAG_FLAVOURS  = "flavours"

CONSTANTS_FILE = f"{TAG_CONSTANTS}.py"
SIGNS_FILE     = f"{TAG_SIGNS}.py"
SPECS_FILE     = f"{TAG_SPECS}.py"
FLAVOURS_FILE  = f"{TAG_FLAVOURS}.py"


TAG_STATUS = "status"
TAG_OK     = "ok"

TAG_BAD_VALIDATION = "bad validation"
TAG_FILE           = "file"

TAG_CRITICAL = "critical"
TAG_WARNING  = "warning"



# --------------- #
# -- TEMPLATES -- #
# --------------- #

TEMPL_CODE_HEADER = """
#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #
""".strip()



# ---------------------- #
# -- LOGGING MESSAGES -- #
# ---------------------- #

###
# XXXXXXX
###
def log_title(
    title,
    desc,
):
    return f"{title.upper()} - {desc}"

###
# XXXXXXX
###
def message_creation_update(
    context,
    upper   = True,
    plurial = True,
):
    if upper:
        context = context.upper()

    plurial = 's' if plurial else ''

    return f"{context} code{plurial}: creation or update."


def raise_validation_error(
    key,
    yfile_name,
    desc,
    xtra = ""
):
    if key:
        key = f"'{key}' key in "

    desc = f"See {key}'{yfile_name}' file: {desc}"

    logging.error(
        log_title(
            TAG_BAD_VALIDATION,
            desc = desc
        )
    )

    if xtra:
        xtra = f" {xtra}"

    raise ValueError(f"{desc}{xtra}")


# ----------- #
# -- PATHS -- #
# ----------- #

def get_specs_folders(
    context,
    this_dir,
    contrib_dir_name,
    nb_step,
    subfolder = "code",
):
    projdir  = this_dir.parent.parent
    projname = projdir.name

    contribdir = projdir / "contrib" / contrib_dir_name / subfolder
    statusdir  = contribdir.parent / "status"
    srcdir     = projdir / "src" / projname / TAG_SPECS / context
    testsdir   = projdir / "tests" / f"{nb_step:02d}-{context}"

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
    context,
    contribdir,
    statusdir,
    subfolder = "",
    ext       = 'py',
):
    logging.info(
        f"{context.upper()} - Looking for accepted contribs."
    )

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


# --------------------- #
# -- PYTHON ANALYSIS -- #
# --------------------- #

def get_metatags(
    allvars,
    vals = META_TAGS
):
    return [
        vname
        for vname in allvars
        if allvars[vname] in vals
    ]


def code_with_metatags(
    allvars,
    metavars,
    code
):
    for name in metavars:
        code = code.replace(f"{allvars[name]!r}", name)

    return code
