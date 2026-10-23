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
#     parser_spec : XXX
#
#     :return: XXX
###
    def extract_parsers(
        self,
        parser_spec
    ):
        return self.split_xor_or(
            data = parser_spec,
            deco = TAG_POST_PROCESS
        )

        data = data.strip()

        if data[-1] == deco:
            use_post_process = True

            data = data[:-1]

        else:
            use_post_process = False

        specs = []

        for p in data.split(TAG_PIP):
            p = p.strip()

            specs.append({
                TAG_TYPE            : TAG_DATA,
                TAG_PARSE_MODULE    : p,
                TAG_USE_POST_PROCESS: use_post_process,
            })

        return specs


###
# prototype::
#     :action: XXX
###
    def split_xor_or(
        self,
        data: str,
        deco: str,
    ) -> set[set[str]]:
        data = data.strip()

        if data[-1] == deco:
            deco_used = True
            data      = data[:-1]

        else:
            deco_used = False

        xor_or_parts = [
            set(
                p.strip()
                for p in part.split(TAG_COMMA)
            )
            for part in data.split(TAG_PIP)
        ]

        return xor_or_parts







###
# prototype::
#     :action: XXX
###
    def build(self):
        self.specs        = dict()
        self.mandatory    = set()
        self.alternative  = set()

        self._last_parser = None

        yaml_specs = safe_load(self.file.read_text())

        from pprint import pprint;pprint(yaml_specs)

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

        raise ValueError('Only list and dict supported for main blocks.')

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
        specs = dict()

        for block_spec, sub_yaml_spec in data_dict.items():
            block_spec = self.split_xor_or(
                data = block_spec,
                deco = TAG_OPTIONAL
            )

            if isinstance(sub_yaml_spec, str):
                sub_yaml_spec = self.extract_parsers(sub_yaml_spec)

            elif isinstance(sub_yaml_spec, dict):
                sub_yaml_spec = self.build_dict(sub_yaml_spec)

            elif isinstance(sub_yaml_spec, list):
                sub_yaml_spec = self.build_list(sub_yaml_spec)

            else:
                raise ValueError('Only str, list and dict supported for sub blocks.')

            specs[f'{block_spec}'] = sub_yaml_spec

        return specs

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

        return _parsers_spec


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
