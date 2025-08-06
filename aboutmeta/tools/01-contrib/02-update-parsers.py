#!/usr/bin/env python3

from collections import defaultdict
from pathlib     import Path
import                  re

from yaml import safe_load


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR     = Path(__file__).parent
PROJECT_DIR  = THIS_DIR.parent.parent
PROJECT_NAME = PROJECT_DIR.name
