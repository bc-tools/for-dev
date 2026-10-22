#!/usr/bin/env python3

from pathlib import Path
import              re
from yaml    import safe_load


from .constants import *

# -------------------------- #
# -- YAML DICT TO PY DICT -- #
# -------------------------- #

###
# prototype::
#     file : XXX
#
#     :return: XXX
###

class DigestedYamlSpecs():
    def __init__(
        self,
        file: Path
    ):
        self.file = file


    def build(self):
        specs = safe_load(self.file.read_text())

        from pprint import pprint;pprint(specs)

        if isinstance(specs, list):
            self.specs = self.build_list(specs)

        elif isinstance(specs, dict):
            self.specs = self.build_dict(specs)

        else:
            raise ValueError('Only list and dict supported.')


    def build_dict(
        self,
        data_dict
    ):
        return {
            TAG_TYPE: TAG_DICT,
        }


    def build_list(
        self,
        data_list
    ):
        if len(data_list) != 1:
            raise ValueError('List must have size 1.')

        parser = data_list[0]

        return {
            TAG_TYPE        : TAG_LIST,
            TAG_PARSE_MODULE: parser,
        }
