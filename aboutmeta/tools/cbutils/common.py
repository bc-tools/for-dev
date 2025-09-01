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
