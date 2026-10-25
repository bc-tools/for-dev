#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))


from itertools   import (
    combinations,
    product,
)

from collections import defaultdict
from dataclasses import dataclass
from benedict    import benedict
from yaml        import safe_load


from cbutils.coding_py import *

from .constants import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

PATTERN_LIST_PARSER = re.compile(r'list\((.*?)\)')


# -------------------------- #
# -- YAML DICT TO PY DICT -- #
# -------------------------- #

###
# prototype::
#     module  : a parser module name.
#     datatype: a data type.
#             @ _ in DATA_TYPES_ALLOWED
#     use_post: do we have to use a post processing.
###
@dataclass
class ParserSpecs():
    module  : str
    datatype: str
    use_post: bool

###
# We check the parser name validity.
###
    def __post_init__(self) -> None:
        validate_pyname(self.module)

        if self.module.startswith('__'):
            raise ValueError(
                 "names staring with '___' are reserved for "
                f"internal processes. See {repr(self.module)}"
            )


type NestedListStrDict = dict[
    str,
    NestedListStrDict | str | list[str]
]

type NestedBoolDict = dict[
    str,
    NestedBoolDict | bool
]

type NestedParserDict = dict[
    str,
    NestedParserDict | ParserSpecs
]


###
# prototype::
#     file : a \yaml file giving a block \specs.
###
class DigestedYamlSpecs():
    def __init__(
        self,
        file: Path
    ) -> None:
        self.file = file

###
# prototype::
#     :action: the \yaml \specs are parsed and the metadata
#              extracted to easily build the \python version
#              of the block \specs.
###
    def build(self) -> None:
        self.reset_attrs()

        specs = self.build_specs(
            yaml_specs = safe_load(self.file.read_text()),
            status     = self.status
        )

        self.specs = {
            self.main_block: specs
        }

###
# prototype::
#     :action: reset the attributes
#              ''self.alts'',
#              ''self.main_block'',
#              ''self.specs'',
#              ''self.status'',
#              ''self._last_parser'' and
#              ''self._prepath_parts''.
###
    def reset_attrs(self) -> None:
        self.main_block = self.file.stem
        self.specs      = dict()
        self.alts       = defaultdict(list)
        self.status     = benedict({
            self.main_block: {
                TAG_MANDATORY: True
            }
        })

        self._last_parser   = ''
        self._prepath_parts = []

###
# prototype::
#     yaml_specs : XXX
#     status     : XXX
#
#     :return: XXX
#
#     :action: XXX
###
    def build_specs(
        self,
        yaml_specs: NestedListStrDict,
        status    : NestedBoolDict,
    ) -> NestedParserDict:
# Depending on the data type used, we call the associated method.
        if isinstance(yaml_specs, dict):
            return self.build_dict(
                data_dict = yaml_specs,
                status    = status
            )

        if isinstance(yaml_specs, list):
            return self.build_list(
                data_list = yaml_specs,
                status    = status
            )

# Unsupported data type in YAML config files.
        raise ValueError(
            'In YAML config files, only list and dict are supported.'
        )

###
# prototype::
#     data_list : XXX
#
#     :return: XXX
#
#
# note::
#      The ''status'' \arg is only included to refactor the code
#      and simplify recursive parsing call coding.
###
    def build_list(
        self,
        data_list: list[str],
        status   : NestedBoolDict,
    ) -> ParserSpecs:
        if len(data_list) != 1:
            raise ValueError(
                'In YAML config files, list of parsers must have '
                'size 1.'
            )

        parsers_spec = self.extract_parser_spec(
            parser_spec = data_list[0]
        )

        if len(parsers_spec) != 1:
            raise ValueError(
                'In YAML config files, only one parser allowed for '
                'a list of data.'
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
    def extract_parser_spec(
        self,
        parser_spec: str,
    ) -> list[ParserSpecs]:
        use_post, parser_spec_extracted = self.split_xor_or(
            data = parser_spec,
            deco = TAG_POST_PROCESS
        )

        final_parser_specs = []

        for pgroup in parser_spec_extracted:
# hhhh
            if len(pgroup) != 1:
                raise ValueError(
                     'In YAML config files, you can use parser '
                    f'choices via a comma. See {repr(parser_spec)}'
                )

# GGG
            parser_name = pgroup.pop()

            match = PATTERN_LIST_PARSER.search(parser_name)

            if match:
                parser_name = match.group(1)
                datatype = TAG_LIST

            else:
                datatype = TAG_STR

# HHHH
            if parser_name == TAG_LAST_PARSER_CARD:
                if not self._last_parser:
                    raise ValueError(
                        'no last parser used'
                    )

                parser_name = self._last_parser

            else:
                self._last_parser = parser_name

# JJJJ
            final_parser_specs.append(
                ParserSpecs(
                    module   = parser_name,
                    datatype = datatype,
                    use_post = use_post,
                )
            )

# Nothing left to do.
        return final_parser_specs

###
# prototype::
#     data : XX
#     deco : XXX
#
#     :return: XXX
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

###
# prototype::
#     data_dict : XXX
#     status    : XXX
#
#     :return: XXX
###
    def build_dict(
        self,
        data_dict,
        status,
    ):
        sub_specs = dict()

        for block_spec, content_spec in data_dict.items():
            is_optional, block_spec = self.split_xor_or(
                data = block_spec,
                deco = TAG_OPTIONAL
            )

            self.update_alts(block_spec)
            self.update_status(
                is_optional,
                block_spec
            )

            if isinstance(content_spec, str):
                self.add_parser_2_blocks(
                    specs        = sub_specs,
                    block_spec   = block_spec,
                    content_spec = content_spec,
                )

                continue

            if isinstance(content_spec, dict):
                next_build = self.build_dict

            elif isinstance(content_spec, list):
                next_build = self.build_list

            else:
                raise ValueError('Only str, list and dict supported for sub blocks.')

            for bgroup in block_spec:
                for bname in bgroup:
                    self._prepath_parts.append(bname)

                    sub_specs[bname] = next_build(
                        content_spec,
                        status = status,
                    )

                    self._prepath_parts.pop(-1)

        return sub_specs

###
# prototype::
#     block_spec : XXX
#
#     :return: XXX
###
    def update_alts(
        self,
        block_spec
    ):
        if len(block_spec) == 1:
            return None

        prepath = '.'.join(self._prepath_parts)

# On doit construire toutes les paires possibles; aide facile pour l'utilisateur (et en plus facile à coder via itertools).
        self.alts[prepath] += [
            set(name_pair)
            for pair_of_sets in combinations(block_spec, 2)
            for name_pair in product(*pair_of_sets)
        ]

###
# prototype::
#     parser_spec : XXX
#
#     :return: XXX
###
    def update_status(
        self,
        is_optional,
        block_spec
    ):
        for bgroup in block_spec:
            for bname in bgroup:
                keypath = self.get_keypath(bname)
                keypath = f'{self.main_block}.{keypath}'

                self.status[keypath] = {
                    TAG_MANDATORY: not is_optional
                }

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
        prefix = '.'.join(self._prepath_parts)

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
    def add_parser_2_blocks(
        self,
        specs,
        block_spec  : list[set[str]],
        content_spec: str,
    ):
        parser_spec = self.extract_parser_spec(
            parser_spec = content_spec
        )

        if len(parser_spec) != len(block_spec):
            if len(parser_spec) != 1:
                raise ValueError('bad len for block name vs parser spec')

            parser_spec = parser_spec*len(block_spec)

        for i, bgroup in enumerate(block_spec):
            for bname in bgroup:
                specs[bname]  = parser_spec[i]
