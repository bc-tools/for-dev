#!/usr/bin/env python3

from pathlib import Path
from yaml    import safe_load

from box import Box

from aboutmeta.parser import (
    date,
    lang,
    license,
    person,
    version,
)

from aboutmeta.specs import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAG_STYLE_DEFAULT = 'default'


# -------------------------------------------------- #
# -- XXXX -- #
# -------------------------------------------------- #

class Extract:
    def __init__(self, style = TAG_STYLE_DEFAULT):
        self.style = style

    def build(self, yaml_file):
        self.data = self.__recu_parse(
            safe_load(yaml_file.read_text()),
            SPECS_PARSING
        )

    def __recu_parse(self, data, specs):
        for key, val in data.items():
            if not key in specs:
                raise KeyError(f"unknown key ''{key}''.")

            # subspecs =specs[key]

            # __recu_parse(self, boxdata, specs)



# xtrct = Extract()
# xtrct.build(Path(__file__).parent.parent.parent / "about.yaml")
