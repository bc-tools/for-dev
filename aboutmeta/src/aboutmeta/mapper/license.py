#!/usr/bin/env python3

from aboutmeta.core.constants import *
from aboutmeta.core.errors    import ParsingError
from aboutmeta.data.license   import License

from json import (
    dumps as json_dumps,
    load  as json_load,
)

from pathlib import Path
import              re

from rapidfuzz import (
    process as fuzz_process,
    fuzz
)


# --------------- #
# -- CONSTANTS -- #
# --------------- #

LICENSES_JSON_FILE = Path(__file__).parent / "parser-license-spdx.json"
