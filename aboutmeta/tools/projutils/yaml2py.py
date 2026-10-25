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


# ----------------------- #
# -- PARSER DATA CLASS -- #
# ----------------------- #

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


# ------------ #
# -- TYPING -- #
# ------------ #

type NestedListStrDictType = dict[
    str,
    NestedListStrDictType | str | list[str]
]

type NestedBoolDictType = dict[
    str,
    NestedBoolDictType | bool
]

type NestedParserDictType = dict[
    str,
    NestedParserDictType | ParserSpecs
]

type ListSetStrType = list[set[str]]


# -------------------------- #
# -- YAML DICT TO PY DICT -- #
# -------------------------- #

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
            safe_load(self.file.read_text())
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
        self.alts       = benedict()
        self.status     = benedict({
            self.main_block: {
                TAG_IS_MANDATORY: True,
            }
        })

        self._last_parser   = ''
        self._prepath_parts = []

###
# prototype::
#     yaml_specs : the \spec \dict extracted from the \yaml file.
#
#     :return: the full digested \spec \dict.
#
#     :action: :see: self.build_dict
#
#     :see: self.build_list ,
#           self.build_dict
###
    def build_specs(
        self,
        yaml_specs: NestedListStrDictType,
    ) -> NestedParserDictType:
# Depending on the data type used, we call the associated method.
        if isinstance(yaml_specs, dict):
            self.status[self.main_block][TAG_IS_PARSED] = False

            return self.build_dict(yaml_specs)

        if isinstance(yaml_specs, list):
            self.status[self.main_block][TAG_IS_PARSED] = True

            return self.build_list(yaml_specs)

# Unsupported data type in the YAML config file.
        raise ValueError(
            'In YAML config files, only list and dict are supported.'
        )

###
# prototype::
#     data_list : an undigested \spec list.
#
#     :return: a single digested list parser.
###
    def build_list(
        self,
        data_list: list[str],
    ) -> ParserSpecs:
# Single list of parsers allowed.
        if len(data_list) != 1:
            raise ValueError(
                'In YAML config files, list of parsers must have '
                'size 1.'
            )

# Analyse the single parser spec.
        parser_spec = self.extract_parser_spec(
            parser_spec = data_list[0]
        )

# No parser choices allowed.
        if len(parser_spec) != 1:
            raise ValueError(
                'In YAML config files, only one parser allowed for '
                'a list of data.'
            )

# We have a legal definition.
        single_parser_spec = parser_spec[0]

# We have to update the type!
        single_parser_spec.datatype = TAG_LIST

# Nothing left to do.
        return single_parser_spec

###
# prototype::
#     parser_spec : an undigested \spec parser.
#
#     :return: a list of alternative digested \spec parsers.
###
    def extract_parser_spec(
        self,
        parser_spec: str,
    ) -> list[ParserSpecs]:
# Extraction of the use-post-process status, and the choices and
# alternatives expected (maybe choices could be useful later).
        use_post, parser_spec_extracted = self.split_xor_or(
            text = parser_spec,
            deco = TAG_POST_PROCESS
        )

# Alternatives of parsers expected.
        parser_spec_alts = []

        for pgroup in parser_spec_extracted:
# No parser choices at this time.
            if len(pgroup) != 1:
                raise ValueError(
                     'In YAML config files, you can use parser '
                    f'choices via a comma. See {repr(parser_spec)}'
                )

# One parser by alternative.
            parser_name = pgroup.pop()

# Taking care of the use of ''list(....)''.
            match = PATTERN_LIST_PARSER.search(parser_name)

            if match:
                parser_name = match.group(1)
                datatype = TAG_LIST

            else:
                datatype = TAG_STR

# Do we must use the last parser name automatically?
            if parser_name == TAG_LAST_PARSER_CARD:
                if not self._last_parser:
                    raise ValueError(
                        'no last parser used'
                    )

                parser_name = self._last_parser

            else:
                self._last_parser = parser_name

# We have a new single parser spec as an alternative.
            parser_spec_alts.append(
                ParserSpecs(
                    module   = parser_name,
                    datatype = datatype,
                    use_post = use_post,
                )
            )

# Nothing left to do.
        return parser_spec_alts

###
# prototype::
#     text : a text
#     deco : a special character that can be used at the end of
#            the text.
#          @ len(deco) = 1
#
#     :return: a pair of \vals.
#              The \1st one indicates whether ''deco'' is used.
#              The \2nd one gives the list of separate pip-part
#              sets, each set obtained by splitting the text by
#              commas.
###
    def split_xor_or(
        self,
        text: str,
        deco: str,
    ) -> (bool, ListSetStrType):
# Do we have a final ''deco'' character?
        text = text.strip()

        if text[-1] == deco:
            deco_used = True
            text      = text[:-1]

        else:
            deco_used = False

# Build the list of separate pip-part sets, each set obtained
# by splitting the part by commas.
        xor_or_parts = [
            set(
                comma_part.strip()
                for comma_part in pip_part.split(TAG_COMMA)
            )
            for pip_part in text.split(TAG_PIP)
        ]

# Nothing left to do.
        return deco_used, xor_or_parts

###
# prototype::
#     data_dict : an undigested \spec dict.
#
#     :return: the digested \spec dict build using ''data_dict''.
#
#     :action: the ''self.status'' and ''self.alts'' \attrs are
#              build.
#
#     :see: self.update_status ,
#           self.update_alts
###
    def build_dict(
        self,
        data_dict: NestedListStrDictType,
    ) -> NestedParserDictType:
        sub_specs = dict()

        for block_spec, parser_spec in data_dict.items():
            is_optional, block_spec = self.split_xor_or(
                text = block_spec,
                deco = TAG_OPTIONAL
            )

# A parser found?
            parser_found = isinstance(parser_spec, str)

# We take care of alternatives, choices and status.
            self.update_alts(block_spec)
            self.update_status(
                parser_found,
                is_optional,
                block_spec
            )

# We have a parser spec.
            if parser_found:
                self.add_parsers_2_blocks(
                    specs        = sub_specs,
                    block_spec   = block_spec,
                    parser_spec = parser_spec,
                )

                continue

# We have either a list, or a dict.
            if isinstance(parser_spec, dict):
                next_build = self.build_dict

            elif isinstance(parser_spec, list):
                next_build = self.build_list

# We have an unsupported type.
            else:
                raise ValueError(
                    'Only str, list and dict supported '
                    'for sub blocks.'
                )

# We store the metadata for all the block without taking care
# of alternatives and choices.
            for bgroup in block_spec:
                for bname in bgroup:
                    self._prepath_parts.append(bname)

                    sub_specs[bname] = next_build(parser_spec)

                    self._prepath_parts.pop(-1)

# Nothing left to do.
        return sub_specs

###
# prototype::
#     block_spec : a digested block \spec.
#
#     :action: update the ''self.alts'' \dict.
###
    def update_alts(
        self,
        block_spec: ListSetStrType,
    ) -> None:
# No alternative....
        if len(block_spec) == 1:
            return None

# Some alternatives.
        if self._prepath_parts:
            blockpath = '.'.join(self._prepath_parts)
            blockpath = f'{self.main_block}.{blockpath}'

        else:
            blockpath = self.main_block

        blockpath = f'{blockpath}.{TAG_ALTS}'

# We need to build all possible pairs; it makes it easy to
# generate a clear error message for the user (and it's easy
# to code using itertools).
        illegal_pairs = [
            set(name_pair)
            for pair_of_sets in combinations(block_spec, 2)
            for name_pair in product(*pair_of_sets)
        ]

        if blockpath in self.alts:
            self.alts[blockpath] += illegal_pairs

        else:
            self.alts[blockpath] = illegal_pairs

###
# prototype::
#     parser_found : ''True'' indicates that the blocks specified in
#                    ''block_spec'' are all for dat to be parsed.
#     is_optional  : ''True'' indicates that the blocks specified
#                    in ''block_spec'' are all optional. Otherwise,
#                    they are all mandatory.
#     block_spec   : :see: self.update_alts
#
#     :action: update the ''self.status'' \dict.
###
    def update_status(
        self,
        parser_found: bool,
        is_optional : bool,
        block_spec  : ListSetStrType,
    ) -> None:
        for bgroup in block_spec:
            for bname in bgroup:
                blockpath = self.get_blockpath(bname)
                blockpath = f'{self.main_block}.{blockpath}'

                self.status[blockpath] = {
                    TAG_IS_MANDATORY: not is_optional,
                    TAG_IS_PARSED   : parser_found,
                }

###
# prototype::
#     blockname : a block name.
#
#     :return: the pointed path of ''blockname'' obtained using
#              the value of ''self._prepath_parts'' at a given
#              time.
###
    def get_blockpath(
        self,
        blockname: str,
    ) -> str:
        prefix = '.'.join(self._prepath_parts)

        if prefix:
            prefix += '.'

        blockpath = f'{prefix}{blockname}'

        return blockpath

###
# prototype::
#     specs       : the \python specifications expected at a
#                   given time.
#     block_spec  : :see: self.update_alts
#     parser_spec : a undigested parser \spec.
#
#     :action: update the ''spec'' \dict by adding new blocks
#              from ''block_spec'' with their parsers.
###
    def add_parsers_2_blocks(
        self,
        specs       : NestedParserDictType,
        block_spec  : ListSetStrType,
        parser_spec: str,
    ) -> None:
        _parser_spec = self.extract_parser_spec(
            parser_spec = parser_spec
        )

        if len(_parser_spec) != len(block_spec):
            if len(_parser_spec) != 1:
                raise ValueError(
                    'Parser and block specs must have the same '
                    'numbers of alternatives, except if the parser '
                    'is alone.'
                )

            _parser_spec = _parser_spec*len(block_spec)

        for i, bgroup in enumerate(block_spec):
            for bname in bgroup:
                specs[bname] = _parser_spec[i]
