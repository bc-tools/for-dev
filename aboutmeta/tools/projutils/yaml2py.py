#!/usr/bin/env python3

from pathlib import Path
import              re
from yaml    import safe_load


from .constants import *


# ------------ #
# -- TYPING -- #
# ------------ #



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
        self.file        = file
        self.specs       = dict()
        self.optional    = []
        self.alternative = []


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
        ...


    def build_list(
        self,
        data_list
    ):
        if len(data_list) != 1:
            raise ValueError('List must have size 1.')

        parser_specs = self.extract_parser(
            data_list[0]
        )

        parser_specs[TAG_TYPE] = TAG_LIST

        return parser_specs


    def extract_parser(
        self,
        parser_spec
    ):
        parser_spec = parser_spec.strip()

        if parser_spec[-1] == TAG_POST_PROCESS:
            use_post_process = True

            parser_spec = parser_spec[:-1]
            parser_spec = parser_spec.strip()

        else:
            use_post_process = False

        return {
            TAG_PARSE_MODULE    : parser_spec,
            TAG_USE_POST_PROCESS: use_post_process,
        }
