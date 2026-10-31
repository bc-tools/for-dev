#!/usr/bin/env python3

from types  import ModuleType
from typing import Callable


from copy    import deepcopy
from pathlib import Path

from benedict import benedict
from yaml     import safe_load


from aboutmeta.core.constants.api_tags      import *
from aboutmeta.core.constants.internal_tags import *

from aboutmeta.core.errors    import *

from aboutmeta.specs.flavour.__ALL_FLAVOURS__ import *



# ------------ #
# -- TYPING -- #
# ------------ #

MULTI_KEYPATH_TYPE = None | str | list[str]

PARSER_TYPE = (
      Callable[[object], object]
    | Callable[[object, object], object]
)


# ------------------ #
# -- CHECKER CLASS --#
# ------------------ #

###
# prototype::
#     amdata : an instance of AMData.
#
#
# This class helps factorize the code: it handles all checks and
# error raising for ''AMData''.
###
class _AMDataChecker:
    def __init__(self, amdata: object) -> None:
        self.amdata = amdata

###
# prototype::
#     _exception : :see: self._raise_kpse_error
#     fmt_str    : a format \str with placeholders to be replaced.
#                  The following placeholders are reserved.
#         + ''{names}'' is used to print a comma separated list of
#           "names".
#         + ''{plural}'' allows to use ''"s"'' for several names,
#           and python::{''} otherwise.
#         + ''{keypath}'', ''{e}'' and ''{etype}'': :see:
#           self._raise_kpse_error.
#     names    : a set of key names.
#     **kwargs : :see: self._raise_kpse_error
#
#     :action: :see: self._raise_kpse_error
#
#
# note::
#     ''lxm'' is the acronym of "list of (e)xtra names".
###
    def _raise_lxm_error(
        self,
        _exception: Exception,
        fmt_str   : str,
        names     : set[str] | list[str],
        **kwargs
    ) -> None:
        sep = ','

        comma_list_names = sep.join([
            f'{self.amdata.get_str_keypath(n)!r}'
            for n in sorted(names)
        ])

        plurial = 's' if sep in comma_list_names else ''

        raise _exception(
            fmt_str.format(
                plurial = plurial,
                names   = comma_list_names,
                **kwargs
            )
        )

###
# prototype::
#     _exception : an exception to raise.
#     fmt_str    : a format \str with placeholders to be replaced.
#                  The following placeholders are reserved.
#         + ''{keypath}'' is replaced by the current ''AMData''
#           full keypath.
#         + ''{e}'' is used to print the sub-exception \msg when
#           present.
#         + ''{etype}'' is the sub-exception type when present.
#     _sub_exception : a caught sub-exception, or ''None'' when
#                      nothing was caught.
#     **kwargs       : optional \args to use as placeholder \vels
#                      in ''fmt_str'' format string.
#
#     :action: raise ''_exception'' using ''fmt_str'' with filled
#              placeholders, appending a suffix for the
#              ''_sub_exception'' message if ''_sub_exception'' is
#              provided.
#
#
# note::
#     ''kpse'' is the acronym of "keypath/sub exception".
###
    def _raise_kpse_error(
        self,
        _exception    : Exception,
        fmt_str       : str,
        _sub_exception: Exception | None = None,
        **kwargs
    ) -> None:
        if _sub_exception is None:
            etype = None

        else:
            etype    = type(_sub_exception).__name__
            fmt_str += ': (sub){etype}: {e}'

        raise _exception(
            fmt_str.format(
                keypath = self.amdata.get_str_keypath(),
                etype   = etype,
                e       = _sub_exception,
                **kwargs
            )
        )

###
# prototype::
#     tolerant : whether to allow main blocks other than flavour
#                ones.
#
#     :action: ensure correct usage of main blocks.
#              When ''tolerant = True'', non-flavour main blocks
#              are also permitted.
###
    def check_main_blocks(
        self,
        tolerant: bool
    ) -> None:
        block_names_used = set(self.amdata._yaml_raw_data)

# Missing mandatory main blocks.
        if not self.amdata._mandatory_block_names <= block_names_used:
            self._raise_lxm_error(
                _exception = ValueError,
                fmt_str    = (
                    'Missing mandatory main block{plurial}: {names}.'
                ),
                names      = (
                      self.amdata._mandatory_block_names
                    - block_names_used
                ),
            )

# Handling of other blocks with or without tolerance.
        if (
            not tolerant
            and
            not block_names_used <= self.amdata._all_block_names
        ):
            self._raise_lxm_error(
                _exception = KeyPathError,
                fmt_str    = (
                    'Unsupported main block{plurial}: {names}.'
                ),
                names      = (
                      block_names_used
                    - self.amdata._all_block_names
                ),
            )

###
# prototype::
#     :action: ensure all keys are used correctly at the current
#              \dict depth.
#
#     :see: self._check_legal_keys ,
#           self._check_no_alt_keys ,
#           self._check_manda_keys
##
    def check_keys(self) -> None:
        self.amdata._current_keys_allowed = set(
            self.amdata._main_parsers[ self.amdata._pre_keylist]
        )

        if self.amdata._pre_keylist in  self.amdata._main_alts:
            self.amdata._current_alts =  self.amdata._main_alts[
                 self.amdata._pre_keylist
            ][TAG_ALTERNATIVES]

        else:
            self.amdata._current_alts = []

        self.amdata._current_status =   self.amdata._main_status[
             self.amdata._pre_keylist
        ]

        self._check_legal_keys()
        self._check_no_alt_keys()
        self._check_manda_keys()

###
# prototype::
#     :action: ensure that only allowed keys are used (at the
#              current \dict depth).
###
    def _check_legal_keys(self) -> None:
        if not (
               self.amdata._current_keys_used
            <= self.amdata._current_keys_allowed
        ):
            self._raise_lxm_error(
                _exception = KeyPathError,
                fmt_str    = 'Illegal key{plurial}: {names}.',
                names      = (
                      self.amdata._current_keys_used
                    - self.amdata._current_keys_allowed
                ),
            )

###
# prototype::
#     :action: ensure that no key alternatives are violated (at
#              the current \dict depth).
###
    def _check_no_alt_keys(self) -> None:
        illegal_couples = set()

        for alt_couple in self.amdata._current_alts:
            if alt_couple <= self.amdata._current_keys_used:
# Later, ''self._raise_lxm_error'' will prefix our '...vs...' text,
# so we have to add it to the 2nd key.
                key_1, key_2 = sorted(alt_couple)
                key_2        = self.amdata.get_str_keypath(key_2)

                illegal_couples.add(f'{key_1} vs {key_2}')

        if illegal_couples:
            self._raise_lxm_error(
                _exception = KeyPathError,
                fmt_str    = (
                    'Illegal couple{plurial} of keys found: {names}.'
                ),
                names      = illegal_couples,
            )

###
# prototype::
#     :action: ensure that no mandatory keys are missing (at
#              the current \dict depth).
###
    def _check_manda_keys(self) -> None:
        mandatory_keys = set()

        for k, v in self.amdata._current_status.items():
            if k in SPECIAL_KEYS:
                continue

            if v[TAG_IS_MANDATORY]:
                mandatory_keys.add(k)

        if not mandatory_keys <= self.amdata._current_keys_used:
            self._raise_lxm_error(
                _exception = KeyPathError,
                fmt_str    = (
                    'Missing mandatory key{plurial}: {names}.'
                ),
                names      = (
                      mandatory_keys
                    - self.amdata._current_keys_used
                ),
            )


# ------------------ #
# -- AMDATA CLASS -- #
# ------------------ #

###
# prototype::
#     flavour : the 'flavour' used to parse data provided by the
#               path::''about.yaml'' file.
#     parent  : the path::''about.yaml'' file folder.
#
#
# note::
#      This class also initializes the following attributes.
#
#          + ''self.yaml_file'' is the full path of the analyzed
#            \yaml file.
#
#          + ''self.data'' stores the data obtained after parsing.
#
#          + ''self.std_yaml_data'' is the standardized version
#            of the data. This allows data standardization without
#            altering the original one (use ''apply_std'' method
#            to apply these changes).
#
#          + ''self.post_vals'' is a dictionary for accessing any
#            values generated by post-processes.
###
class AMData:
###
# prototype::
#     :return: a new instance of the ''AMData'' class. This allows
#              working with instances without importing ''amdata''.
#
#
# note::
#     This method is used by postprocessing functions.
###
    @classmethod
    def new_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __init__(
        self,
        flavour: str,
        parent : Path,
    ) -> None:
        self._checker = _AMDataChecker(self)

        self.flavour = flavour
        self.parent  = parent

###
# We define ''getter'' and ''setter'' for the ''flavour'' \attr.
###
    @property
    def flavour(self) -> str:
        return self._flavour

###
# prototype::
#     flavour : :see: AMData
#             @ flavour in ALL_FLAVOURS
#
#     :action: set \attrs needed to work with ''flavour''.
###
    @flavour.setter
    def flavour(
        self,
        flavour: str
    ) -> None:
        if not flavour in ALL_FLAVOURS:
            raise ValueError(f'unknow flavour {flavour!r}.')

        self._flavour       = flavour
        self._flavour_specs = ALL_FLAVOURS[flavour]

        self._all_block_names       = set()
        self._mandatory_block_names = set()

        for bname in self._flavour_specs:
            self._all_block_names.add(bname)

            if self._flavour_specs[bname][TAG_IS_MANDATORY]:
                self._mandatory_block_names.add(bname)

###
# We define ''getter'' and ''setter'' for the ''parent'' \attr.
###
    @property
    def parent(self) -> Path:
        return self._parent

###
# prototype::
#     parent : :see: AMData
#
#     :action: validate the existence of the ''parent'' folder
#              and the path::''about.yaml'' file.
###
    @parent.setter
    def parent(
        self,
        parent: Path
    ) -> None:
        if not parent.is_dir():
            raise IOError(f"Missing folder '{parent}'.")

        yaml_file = parent / TAG_ABOUT_YAML

        if not yaml_file.is_file():
            raise IOError(f"Missing file '{yaml_file}'.")

        self._parent   = parent
        self.yaml_file = yaml_file

###
# prototype::
#     tolerant : ''True'' requests to accept additional main
#                blocks that will be silently ignored.
#                With ''False'', additional main blocks blocks
#                are rejected.
#
#     :return: the data parsed into a dictionary which mimics
#              the \yaml file.
#
#     :see: self._recu_build
###
    def build(
        self,
        tolerant: bool = True
    ) -> benedict:
# Data operations (e.g., write, normalize, ...) require the full
# 'keypaths' to the data.
        self._full_data_keypaths = []

# Retrieving data from the YAML file.
        self._yaml_raw_data = safe_load(
            self.yaml_file.read_text()
        )

        if not type(self._yaml_raw_data) == dict:
            dtype = type(self._yaml_raw_data).__name__

            raise ValueError(
                f'{TAG_ABOUT_YAML!r} file must use '
                f'a main dictionary: {dtype!r} found.'
            )

# Check the main-block names used.
        self._pre_keylist = []

        self._checker.check_main_blocks(tolerant)

# Analysis of the content of each main block.
        data = dict()

        for block, content in self._yaml_raw_data.items():
# A main block to ignore?
            if (
                tolerant
                and
                not block in self._all_block_names
            ):
                continue

# Content has to be analyzed.
            self._pre_keylist = [block]

            specs = self._flavour_specs[block]

            self._main_parsers = specs[TAG_BLOCK_PARSERS]
            self._main_status  = specs[TAG_BLOCK_STATUS]
            self._main_alts    = specs[TAG_BLOCK_ALTS]

            data[block] = self._recu_build(content)

# Job has been done, we can deliver a ''benedict'' object.
        self.data = benedict(data)

###
# prototype::
#     raw_data : a \dict to be parsed.
#
#     :return: a \dict of parsed data.
#
#     :see: self._build_list ,
#           self._recu_build_dict
###
    def _recu_build(
        self,
        raw_data: dict | list,
    ) -> dict:
# List of data. This case ONLY occurs for main blocks!
        if isinstance(raw_data, list):
            datatype = self._this_data_type()

            if datatype != TAG_LIST:
                kp = self.get_str_keypath()

                self._checker._raise_kpse_error(
                    _exception = ValueError,
                    fmt_str    = (
                        'Block {keypath!r} does not expect a list '
                        'of data to parse.'
                    ),
                )

            return self._build_list(raw_data)

# Dict recursively parsed.
        elif isinstance(raw_data, dict):
            return self._recu_build_dict(raw_data)

# Unknown use case unimplemented.
        else:
            self._checker._raise_kpse_error(
                dtype      = type(raw_data).__name__,
                _exception = ValueError,
                fmt_str    = (
                    'Unsupported YAML content with Python type '
                    '{dtype!r}. See key {keypath!r}.'
                ),
            )

###
# prototype::
#     raw_data : a \list to be parsed.
#
#     :return: a \list with the parsed data.
###
    def _build_list(
        self,
        raw_data: list,
    ) -> list:
        self._update_full_data_keypaths()

        data          = []
        parser_module = self._this_parser_module()

        for pos, rd in enumerate(raw_data, start = 1):
            try:
                data.append(
                    self._get_parsed_data(
                        raw_data      = rd,
                        parser_module = parser_module,
                    )
                )

            except Exception as e:
                kp = self.get_str_keypath()

                self._checker._raise_kpse_error(
                    _sub_exception = e,
                    pos            = pos,
                    _exception     = ParsingError,
                    fmt_str        = (
                        'Block {keypath!r} has invalid item list '
                        'data at position {pos}: {etype}: {e}'
                    ),
                )

# Nothing left todo.
        return data

###
# prototype::
#     raw_data : a \dict to be parsed.
#
#     :return: a \dict with the parsed data.
###
    def _recu_build_dict(
        self,
        raw_data: dict,
    ) -> dict:
        data = dict()

# Checking good use of keys.
        self._current_keys_used = set(raw_data)

        self._checker.check_keys()

# Now, we work with legal keys.
        for key, val in raw_data.items():
# Stack current key. OpenGL has infected me! :-)
            self._pre_keylist.append(key)

# A data type?
            datatype = self._this_data_type()

# A value to build recursively.
            if datatype is None:
                new_val = self._recu_build(val)

# A list of values to build.
            elif datatype == TAG_LIST:
                new_val = self._build_list(val)

# A single value to parse.
            else:
                self._update_full_data_keypaths()

                new_val = self._get_parsed_data(
                    raw_data      = val,
                    parser_module = self._this_parser_module(),
                )

# All work has been done!
            data[key] = new_val

# Pop the key from the key path.
            self._pre_keylist.pop(-1)

# Nothing left todo.
        return data

###
# prototype::
#     raw_data      : a single data to be parsed.
#     parser_module : a parser module.
#
#     :return: data parsed by the ''parse'' \func of the module
#              ''parser_module''.
###
    def _get_parsed_data(
        self,
        raw_data     : object,
        parser_module: ModuleType,
    ) -> object:
# Only string allowed!
        if parser_module == str:
            if not type(raw_data) == str:
                raise ParsingError(
                    f'{raw_data!r} is not a string.'
                )

            return raw_data

# One data to parse by using the good signature.
        amdata_use, _ = self._this_amdata_use()

        try:
            if amdata_use:
                return parser_module.parse(
                    amdata = self,
                    data   = raw_data
                )

            return parser_module.parse(raw_data)

        except Exception as e:
            self._checker._raise_kpse_error(
                _exception     = ParsingError,
                fmt_str        = 'Invalid data {raw_data!r}',
                _sub_exception = e,
            )

###
# prototype::
#     key : a \yaml key.
#
#     :return: the full "keypath" to access the ''key'' data (at
#              the current dictionary depth).
###
    def get_str_keypath(
        self,
        key: str = ''
    ) -> str:
        if self._pre_keylist:
            keypath = '.'.join(self._pre_keylist)

            if key:
                keypath += f'.{key}'

        else:
            keypath = key

        return keypath

###
# prototype::
#     :action: only for data, append the current keypath to
#              the list ''self._full_data_keypaths''.
###
    def _update_full_data_keypaths(self) -> None:
        self._full_data_keypaths.append(
            self.get_str_keypath()
        )

###
# prototype::
#     :return: a data type if the current "keylist" points to
#              a data, ''None'' otherwise.
#            @ _ in ALLTAGS_DATATYPES or _ = None
###
    def _this_data_type(self) -> str | None:
        return self._main_parsers[self._pre_keylist].get(
            TAG_DATATYPE,
            None
        )

###
# prototype::
#     tag : a tag to retrieve metadata from the \specs of the
#              current "keylist".
#
#     :return: \spec metadata associated to "keylist".
###
    def _get_current_metadata(
        self,
        tag: str,
    ) -> dict:
        return self._main_parsers[self._pre_keylist][tag]

###
# prototype::
#     :return: the \python parsing module of the current
#              "keylist" parser.
###
    def _this_parser_module(self) -> ModuleType:
        return self._get_current_metadata(TAG_PARSER)

###
# prototype::
#     :return: ''amdata''-\arg \specs of the current "keylist"
#              parser.
###
    def _this_amdata_use(self) -> (bool, bool | None):
        return self._get_current_metadata(TAG_AMDATA_USE)

###
# prototype::
#     :return: ''True'' if post-processing is proposed by the
#              current "keylist" parser, ''False'' otherwise.
###
    def _this_use_post(self) -> bool:
        return self._get_current_metadata(TAG_USE_POST)

###
# prototype::
#     keypath : this \arg can be of three types.
#         1. ''None'' asks to iterate on all the data
#            "keypaths".
#         1. A string value allows you to use a specific
#            "keypath".
#         1. A list of string values iterate for specific
#            "keypaths".
#
#     :yield: at each iteration, three values are yielded.
#         1. The current data "keypath".
#         1. The data associated with the "keypath".
#         1. The parser to apply to the data.
###
    def _iter_keypath(
        self,
        keypath: MULTI_KEYPATH_TYPE = None,
    ) -> (str, object, PARSER_TYPE):
# We want to work with a list of keypaths.
        if keypath is None:
            keypaths_wanted = self._full_data_keypaths

        elif type(keypath) == str:
            keypaths_wanted = [keypath]

        else:
            keypaths_wanted = keypath

# Let's walk together on a flat land.
        for kp in keypaths_wanted:
            if not kp in self._full_data_keypaths:
                raise KeyPathError(f'Broken keypath {kp!r}.')

            yield (
                kp,
                self.data[kp],
                self._main_parsers[kp][TAG_PARSER]
            )

###
# prototype::
#     keypath : :see: self._iter_keypath
#
#     :action: ''self.std_yaml_data'' matches the original \yaml
#              \dict, but with standardized \vals corresponding
#              to the desired "keypaths".
###
    def standardize(
        self,
        keypath: MULTI_KEYPATH_TYPE = None,
    ) -> None:
        self.std_yaml_data = benedict()

        for kp, val, parser_module in self._iter_keypath(keypath):
# String immutability.
            if parser_module == str:
                std_yaml_val = val

# Otherwise we have a write function.
            else:
                std_yaml_val = parser_module.write(val)

# Let's store the standard YAML version.
            self.std_yaml_data.set(kp, std_yaml_val)

###
# prototype::
#     keypath : :see: self._iter_keypath
#
#     :action: normalize all the data \vals of ''self.data''
#              corresponding to the desired "keypaths".
#
#     :see: self._normalize_me
###
    def normalize(
        self,
        keypath: MULTI_KEYPATH_TYPE = None,
    ) -> None:
        for _ , val, _ in self._iter_keypath(keypath):
            if type(val) == list:
                for elt in val:
                    self._normalize_me(elt)

            else:
                self._normalize_me(val)

###
# prototype::
#     data : a data object.
#
#     :action: if ''data'' has a ''normalize'' \attr, it is
#              called as a zero-\arg \func.
###
    def _normalize_me(
        self,
        data: object,
    ) -> None:
        if hasattr(data, 'normalize'):
            data.normalize()

###
# prototype::
#     keypath  : :see: self._iter_keypath
#     tolerant : :see: _AMDataChecker.check_main_blocks
#
#     :action: launch the post-processing of all the data \vals
#              of ''self.data'' corresponding to the desired
#              "keypaths".
#              When ''tolerant = True'', missing post-processing
#              \feats are silently ignored, otherwise, an error
#              is raised.
#
#     :return: a \dict providing access to any data returned by
#              the called post-processors.
###
    def postprod(
        self,
        keypath : MULTI_KEYPATH_TYPE = None,
        tolerant: bool = True,
    ) -> benedict:
        results_captured = benedict()

# Let's call the desired post-processing.
        for kp , val, parser_module in self._iter_keypath(keypath):
            if not self._main_parsers[kp][TAG_USE_POST]:
                if not tolerant:
                    self._checker._raise_kpse_error(
                        _exception = KeyPathError,
                        fmt_str    = (
                            'No post-processing for {keypath!r}.'
                        ),
                    )

                continue

            _ , amdata_use = self._main_parsers[kp][TAG_AMDATA_USE]

            try:
                if amdata_use:
                    result = parser_module.postprod(
                        amdata = self,
                        data   = val
                    )

                else:
                    result = parser_module.postprod(val)

            except Exception as e:
                self._checker._raise_kpse_error(
                    _exception     = PostProcessingError,
                    fmt_str        = 'Post processing of {kp!r}',
                    _sub_exception = e,
                )

            if not result is None:
                for tag in result:
                    if tag in results_captured:
                        self._checker._raise_kpse_error(
                            _exception = CriticalImplementationError,
                            fmt_str    = (
                                'Post prod tag {tag!r} has been used '
                                'twice. Found with data {keypath!r}.'
                            ),
                            tag        = tag
                        )

                results_captured |= result

# Nothing left to do.
        return results_captured


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# What I test.
    TEST_WANTED = [
        1, # Only project.
        2, # Only atoc.
    ]

# Let's go.
    from pprint import pprint

    projdir = Path(__file__).parent

    while projdir.name != 'for-dev':
        projdir = projdir.parent

# Only project.
    if 1 in TEST_WANTED:
        myflavour = TAG_IT_PROJECT
        mydir     = projdir / 'aboutmeta'

        amdata = AMData.new_instance(
            flavour = myflavour,
            parent  = mydir,
        )

        amdata.build()

        print()
        print(f'All keypaths: {amdata._full_data_keypaths}')

        first_data = amdata.data[amdata._full_data_keypaths[0]]

        print()
        print(f'1st data: {first_data}')
        print(f'    repr: {first_data!r}')

        print()
        print('Data parsed')
        print(amdata.data.to_json(indent = 4))

        print()
        print('Standardize')

        amdata.standardize()
        print(amdata.std_yaml_data.to_yaml(indent = 2))

        print()
        print('Normalize')

        amdata.normalize()

        print(amdata.data.to_json(indent = 4))

        print()
        print('Post processing')

        amdata.postprod()

        results = amdata.postprod()

        print(results)

# Only atoc.
    if 2 in TEST_WANTED:
        myflavour = TAG_ATOC
        mydir     = (
              projdir
            / 'aboutmeta' / 'contribute' / 'api'
            / 'parser' / 'readme'
        )

        amdata = AMData.new_instance(
            flavour = myflavour,
            parent  = mydir,
        )

        amdata.build()

        print()
        print(f'All keypaths: {amdata._full_data_keypaths}')

        print()
        print('Data parsed')

        print(amdata.data.to_json(indent = 4))

        print()
        print('Post processing')

        results = amdata.postprod()

        print(results.to_json(indent = 4))

        for i, p in enumerate(results[TAG_POSTPROD_ABOUT_PATH_FILES], start = 1):
            print(f'{i}: {p.relative_to(projdir)}')
