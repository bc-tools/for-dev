#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))


from collections import defaultdict
from dataclasses import dataclass
from yaml        import safe_load

from cbutils.coding_py import *

from .constants import *


# ------------ #
# -- TYPING -- #
# ------------ #

PATTERN_LIST_PARSER = re.compile(r'list\((.*?)\)')


# -------------------------- #
# -- YAML DICT TO PY DICT -- #
# -------------------------- #

###
# prototype::
#     file : XXX
###
@dataclass
class ParserSpecs():
    module  : str
    datatype: str
    use_post: bool

    def __post_init__(self) -> None:
        validate_pyname(self.module)

        if self.module == TAG_OPTIONAL:
            raise ValueError(
                f'Illegal paser name {repr(TAG_OPTIONAL)} (reserved for internal processe)'
            )


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
#     :action: the \yaml \specs are parsed and the metadata
#              extracted to easily build the \python version
#              of the block \specs.
###
    def build(self):
        self.reset_attrs()

        yaml_specs = safe_load(self.file.read_text())

        specs = self.build_specs(yaml_specs)

        self.specs = {
            self.main_block: specs
        }

###
# prototype::
#     :action: reset the attributes
#              ''self.alts'',
#              ''self.mandatory'',
#              ''self.specs'',
#              ''self._last_parser'' and
#              ''self._prepath''.
###
    def reset_attrs(self):
        self.main_block = self.file.stem
        self.specs      = dict()
        self.mandatory  = dict()
        self.alts       = dict()

        self._last_parser = ''
        self._prepath     = []







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
        if isinstance(yaml_specs, dict):
            return self.build_dict(yaml_specs)

        if isinstance(yaml_specs, list):
            return self.build_list(yaml_specs)

        raise ValueError('Only list and dict supported for main blocks.')


# prototype::
#     specs : XXX
#
#     :return: XXX
###
    def update_mandatory(
        self,
        block_group
    ):
        ...





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
            is_optional, block_spec = self.split_xor_or(
                data = block_spec,
                deco = TAG_OPTIONAL
            )

            if len(block_spec) != 1:
                self.alts.append(
                    set(
                        self.get_keypath(bname)
                        for bgroup in block_spec
                        for bname in bgroup
                    )
                )


            if isinstance(sub_yaml_spec, str):
                self.add_parser_2_blocks(
                    specs         = specs,
                    is_optional   = is_optional,
                    block_spec    = block_spec,
                    sub_yaml_spec = sub_yaml_spec,
                )

                continue

            if isinstance(sub_yaml_spec, dict):
                next_build = self.build_dict

            elif isinstance(sub_yaml_spec, list):
                next_build = self.build_list

            else:
                raise ValueError('Only str, list and dict supported for sub blocks.')

            for grp in block_spec:
                for b in grp:
                    self._prepath.append(b)

                    specs[b] = next_build(sub_yaml_spec)

                    self._prepath.pop(-1)

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

        parsers_spec = self.extract_parser_spec(
            data_list[0]
        )

        if len(parsers_spec) != 1:
            raise ValueError(
                'Only one parser by list of data.'
            )

        parser_spec = parsers_spec[0]

# We have to update the type!
        parser_spec.datatype = TAG_LIST

        return parser_spec





###
# prototype::
#     parser_spec : XXX
#
#     :return: XXX
###
    def add_parser_2_blocks(
        self,
        specs,
        is_optional  : bool,
        block_spec   : list[set[str]],sub_yaml_spec: str,
    ):
        parser_spec = self.extract_parser_spec(
            parser_spec = sub_yaml_spec
        )

        if len(parser_spec) != len(block_spec):
            if len(parser_spec) != 1:
                raise ValueError('bad len for block name vs parser spec')

            parser_spec = parser_spec*len(block_spec)

        for i, bgroup in enumerate(block_spec):
            current_depth = len(self._prepath)

            if not is_optional:
                self.mandatory[current_depth] |= set(
                    self.get_keypath(bname)
                    for bname in bgroup
                )

            for bname in bgroup:
                specs[bname] = parser_spec[i]





###
# prototype::
#     parser_spec : XXX
#
#     :return: XXX
###
    def get_keypath(
        self,
        key: str,
    ):
        prefix = '.'.join(self._prepath)

        if prefix:
            prefix += '.'

        keypath = f'{prefix}{key}'

        return keypath




###
# prototype::
#     parser_spec : XXX
#
#     :return: XXX
###
    def extract_parser_spec(
        self,
        parser_spec
    ):
        use_post_process, parser_spec = self.split_xor_or(
            data = parser_spec,
            deco = TAG_POST_PROCESS
        )

        final_parser_spec = []

        for pgroup in parser_spec:
            if len(pgroup) != 1:
                raise ValueError(
                    f'pas de virgule pour els parsers: {pgroup=}'
                )

            parser_name = pgroup.pop()

            match = PATTERN_LIST_PARSER.search(parser_name)

            if match:
                parser_name = match.group(1)
                parser_type = TAG_LIST

            else:
                parser_type = TAG_STR

            if parser_name == TAG_LAST_PARSER_CARD:
                if not self._last_parser:
                    raise ValueError(
                        'no last parser used'
                    )

                parser_name = self._last_parser

            else:
                self._last_parser = parser_name

            final_parser_spec.append(
                ParserSpecs(
                    module   = parser_name,
                    datatype = parser_type,
                    use_post = use_post_process,
                )
            )

        return final_parser_spec

###
# prototype::
#     :action: XXX
###
    def split_xor_or(
        self,
        data: str,
        deco: str,
    ) -> (bool, list[set[str]]):
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

        return deco_used, xor_or_parts
