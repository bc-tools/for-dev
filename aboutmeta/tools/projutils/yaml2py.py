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
###

class DigestedYamlSpecs():
    def __init__(
        self,
        file: Path
    ):
        self.file = file

###
# prototype::
#     :action: XXX
###
    def build(self):
        self.specs        = dict()
        self.optional     = set()
        self.alternative  = set()
        self._last_parser = None

        yaml_specs = safe_load(self.file.read_text())

        specs = self.build_specs(yaml_specs)

        self.specs = {
            self.file.stem: specs
        }

###
# prototype::
#     specs : XXX
#
#     :return: XXX
###
    def build_specs(
        self,
        yaml_specs
    ):
        if isinstance(yaml_specs, list):
            return self.build_list(yaml_specs)

        if isinstance(yaml_specs, dict):
            return self.build_dict(yaml_specs)

        raise ValueError('Only list and dict supported.')

###
# prototype::
#     data_dict : XXX
#
#     :return: XXX
###
    def build_dict(
        self,
        data_dict
    ):
        for block_spec, sub_yaml_spec in data_dict.items():
            print('---')
            print(f"{   block_spec = }")
            print(f"{sub_yaml_spec = }")

###
# prototype::
#     data_list : XXX
#
#     :return: XXX
###
    def build_list(
        self,
        data_list
    ):
        if len(data_list) != 1:
            raise ValueError(
                'List of parsers must have size 1.'
            )

        _parsers_spec = self.extract_parsers(
            data_list[0]
        )

        if len(_parsers_spec) != 1:
            raise ValueError(
                'Only one parser by list of data.'
            )

        parser_spec = _parsers_spec[0]

# We have to update the type!
        parser_spec[TAG_TYPE] = TAG_LIST

        return parser_spec

###
# prototype::
#     XXX : XXX
#
#     :return: XXX
###
    def extract_blocks(
        self,
    ):
        ...

###
# prototype::
#     parser_spec : XXX
#
#     :return: XXX
###
    def extract_parsers(
        self,
        parser_spec
    ):
        parser_spec = parser_spec.strip()

        if parser_spec[-1] == TAG_POST_PROCESS:
            use_post_process = True

            parser_spec = parser_spec[:-1]

        else:
            use_post_process = False

        specs = []

        for p in parser_spec.split(TAG_PIP):
            p = p.strip()

            specs.append({
                TAG_TYPE            : TAG_DATA,
                TAG_PARSE_MODULE    : p,
                TAG_USE_POST_PROCESS: use_post_process,
            })

        return specs
