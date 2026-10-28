#!/usr/bin/env python3


# extract en mode cool : on veut juste un dict avec els cles des blocs et d'autres en plus ok
# extract(soft=False) pour mode strict

# postprod() : pour tous ces qu'i peut l'etre : résultat stocké dans un dict dédié

# posprod(keypath) : pour un sous jeu de donné ou une donné

from types import ModuleType


from pathlib import Path

from benedict import benedict
from yaml     import safe_load

from aboutmeta.core.constants                 import *
from aboutmeta.core.errors                 import ParsingError
from aboutmeta.specs.flavour.__ALL_FLAVOURS__ import *


###
# prototype::
#     flavour : hhh
#     parent  : ggg
#
#
# note::
#     This class also builds the following attributes.
#
#         + ''self.yaml_file''
#
#         + ''self.data''
#
#         + ''self.std_data''
#
#         + ''self.post_vals''
###
class AMData:
    @classmethod
    def new_instance(cls, **kwargs):
        return cls(**kwargs)

    def __init__(
        self,
        flavour: str,
        parent : Path,
    ):
        self.flavour = flavour
        self.parent  = parent

###
# We define a getter and a setter for the attribute ''flavour''.
###
    @property
    def flavour(self) -> str:
        return self._flavour

###
# prototype::
#     flavour : :see: AMData
#
#     :action: JJJJ
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
# We define a getter and a setter for the attribute ''parent''.
###
    @property
    def parent(self) -> str:
        return self._parent

###
# prototype::
#     parent : :see: AMData
#
#     :action: JJJJ
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
#     tolerent : hhh
#
#     :return: ''benedict'' version of the data parsed.
###
    def build(
        self,
        tolerent: bool = True
    ) -> benedict:
# Liste des chemins des clés à nourrir lors du build.
        self._all_data_keypaths = []

# Dict des données
        self._yaml_raw_data = safe_load(
            self.yaml_file.read_text()
        )

        if not type(self._yaml_raw_data) == dict:
            _type = type(self._yaml_raw_data).__name__

            raise ValueError(
                f'{TAG_ABOUT_YAML!r} file must use '
                f'a main dictionary: {_type!r} found.'
            )

# Check the names used.
        self._check_main_blocks(tolerent)


# Trvaille sur chque main blcok
        data = dict()

        for k, v in self._yaml_raw_data.items():
            if (
                tolerent
                and
                not k in self._all_block_names
            ):
                continue

            self._pre_keypath = [k]

            specs = self._flavour_specs[k]

            self._main_parsers = specs[TAG_BLOCK_PARSERS]
            self._main_status  = specs[TAG_BLOCK_STATUS]
            self._main_alts    = specs[TAG_BLOCK_ALTS]

            data[k] = self._recu_build(v)

        self.data = benedict(data)

###
# prototype::
#     raw_data : Y
#
#     :return: Z
###
    def _recu_build(
        self,
        raw_data: dict | list,
    ) -> dict:
# List of data ONLY for a main block!
        if isinstance(raw_data, list):
            datatype = self._main_parsers[self._pre_keypath].get(
                TAG_DATATYPE,
                None
            )

            if datatype != TAG_LIST:
                raise ValueError(
                    f'Block {self._get_str_keypath()!r} does not '
                    'expect a list of data to parse.'
                )

            return self._build_list(raw_data)

# Can be recurively called.
        elif isinstance(raw_data, dict):
            return self._recu_build_dict(raw_data)

# Unknow usecase unimplemented.
        else:
            _type   = type(raw_data).__name__
            keypath = self._get_str_keypath()

            raise ValueError(
                f'Unsupported yaml content Python typed {_type!r}. '
                f'See key {keypath!r}.'
            )

###
# prototype::
#     raw_data : Y
#
#     :return: Z
###
    def _build_list(
        self,
        raw_data: list,
    ) -> list:
        self._update_all_data_keypaths()

        data          = []
        parser_module = self._this_parser_module()

        for pos, rd in enumerate(raw_data, start = 1):
            try:
                data.append(
                    self._get_parsed_data(
                        raw_data = rd,
                        parser_module = parser_module,
                    )
                )

            except Exception as e:
                raise ParsingError(
                    f'Block {self._get_str_keypath()!r} has invalid item list data at position {pos}: {type(e).__name__}: {e}'
                )

# Nothing left todo.
        return data

###
# prototype::
#     raw_data : Y
#
#     :return: Z
###
    def _recu_build_dict(
        self,
        raw_data: dict,
    ) -> dict:
        data = dict()

# Checing good use of keys.
        self._current_keys_used    = set(raw_data)
        self._current_keys_allowed = set(
            self._main_parsers[
                self._pre_keypath
            ]
        )

        if self._pre_keypath in self._main_alts:
            self._current_alts = self._main_alts[
                self._pre_keypath
            ][TAG_ALTERNATIVES]

        else:
            self._current_alts = []

        self._current_status =  self._main_status[
            self._pre_keypath
        ]

        self._check_legal_keys()
        self._check_no_alt_keys()
        self._check_manda_keys()

# Now, we work with legal keys.
        for key, val in raw_data.items():
# Stack current key. OpenGL has infected me! :-)
            self._pre_keypath.append(key)

# A data type?
            datatype = self._main_parsers[self._pre_keypath].get(
                TAG_DATATYPE,
                None
            )

# A value to build recursively.
            if datatype is None:
                new_val = self._recu_build(val)

            else:
                parser_module = self._this_parser_module()

# A list of values to build.
                if datatype == TAG_LIST:
                    new_val = self._build_list(val)

# A value to parse (datatype captured before).
                else:
                    self._update_all_data_keypaths()

                    new_val = self._get_parsed_data(
                        raw_data      = val,
                        parser_module =     parser_module,
                    )

# All work has been done!
            data[key] = new_val

# Pop the key from the key path.
            self._pre_keypath.pop(-1)

# Nothing left todo.
        return data


###
# prototype::
#     raw_data      : Y
#     parser_module : Y
#
#     :action: Z
###
    def _update_all_data_keypaths(self):
        self._all_data_keypaths.append(
            self._get_str_keypath()
        )

###
# prototype::
#     raw_data      : Y
#     parser_module : Y
#
#     :return: Z
###
    def _get_parsed_data(
        self,
        raw_data,
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
        amdata_use, _ = self._this_parser_amdata_use()

        try:
            if amdata_use:
                return parser_module.parse(
                    amdata = self,
                    data   = raw_data
                )

            else:
                return parser_module.parse(raw_data)

        except Exception as e:
            raise ParsingError(
                f'Invalid data {raw_data!r} raises: {type(e).__name__}: {e}'
            )

###
# prototype::
#     key : Y
#
#     :return: Z
###
    def _get_current_parser_metadata(
        self,
        key: str,
    ) -> object:
        return self._main_parsers[self._pre_keypath][key]

###
# prototype::
#     :return: Z
###
    def _this_parser_amdata_use(self) -> (bool, bool | None):
        return self._get_current_parser_metadata(TAG_AMDATA_USE)

###
# prototype::
#     :return: Z
###
    def _this_parser_module(self) -> ModuleType:
        return self._get_current_parser_metadata(TAG_PARSER)

###
# prototype::
#     :return: Z
###
    def _this_parser_use_post(self) -> bool:
        return self._get_current_parser_metadata(TAG_USE_POST)

###
# prototype::
#     :action: Z
###
    def _check_legal_keys(self) -> None:
        if not self._current_keys_used <= self._current_keys_allowed:
            plurial, names = self._msg_list_names(
                self._current_keys_used - self._current_keys_allowed
            )

            raise KeyError(
                f'Illegal key{plurial}: {names}.'
            )

###
# prototype::
#     :action: Z
###
    def _check_no_alt_keys(self) -> None:
        illegal_couples = set()

        for alt_couple in self._current_alts:
            if alt_couple == (
                alt_couple & self._current_keys_used
            ):
                illegal_couples.add(
                    ' vs '.join(sorted(alt_couple))
                )

        if illegal_couples:
            plurial, names = self._msg_list_names(
                illegal_couples
            )

            raise KeyError(
                f'Illegal couple{plurial} of keys found: '
                f'{names}.'
            )

###
# prototype::
#     :action: Z
###
    def _check_manda_keys(self) -> None:
        mandatory_keys = set()

        for k, v in self._current_status.items():
            if k in SPECIAL_KEYS:
                continue

            if v[TAG_IS_MANDATORY]:
                mandatory_keys.add(k)

        if not mandatory_keys <= self._current_keys_used:
            plurial, names = self._msg_list_names(
                mandatory_keys - self._current_keys_used
            )

            raise KeyError(
                f'Missing mandatory key{plurial}: '
                f'{names}.'
            )

###
# prototype::
#     tolerent : Y
#
#     :action: Z
###
    def _check_main_blocks(
        self,
        tolerent: bool
    ) -> None:
        block_names_used = set(self._yaml_raw_data)

# Missing mandatory main blocks.
        if not self._mandatory_block_names <= block_names_used:
            plurial, names = self._msg_list_names(
                self._mandatory_block_names - block_names_used
            )

            raise ValueError(
                f'Missing mandatory main block{plurial}: {names}.'
            )

# Pas d'autres blocs principaux
        if (
            not tolerent
            and
            not block_names_used <= self._all_block_names
        ):
            plurial, names = self._msg_list_names(
                block_names_used - self._all_block_names
            )

            raise ValueError(
                f'Unsupported main block{plurial}: {names}.'
            )

###
# prototype::
#     key : Y
#
#     :return: Z
###
    def _get_str_keypath(
        self,
        key: str = ''
    ) -> str:
        keypath = '.'.join(self._pre_keypath)

        if key:
            keypath += f'.{key}'

        return keypath

###
# prototype::
#     names : Y
#     sep   : Y
#
#     :return: Z
###
    def _msg_list_names(
        self,
        names: set[str],
        sep  : str = ', '
    ) -> (str, str):
        list_names = sep.join([
            f'{self._get_str_keypath(n)!r}'
            for n in sorted(names)
        ])

        plurial = 's' if sep in list_names else ''

        return plurial, list_names

###
# prototype::
#     keypath : Y
#
#     :return: Z
###
    def standardize(
        self,
        keypath: None | str | list[str] = None,
    ) -> dict:
        self.std_data = benedict()

        for kp, val, parser_module in self._iter_keypath(keypath):
# String immbilsim...
            if parser_module == str:
                std_yaml_val = val

# Otherwise we have a write function.
            else:
                std_yaml_val = parser_module.write(val)

            self.std_data.set(kp, std_yaml_val)


###
# prototype::
#     keypath : Y
#
#     :return: Z
#
#     :action: Z
###
    def postprod(
        self,
        keypath: str | list[str] = '',
    ) -> dict:
        ...




###
# prototype::
#     keypath : Y
#
#     :yield: Z
###
    def _iter_keypath(
        self,
        keypath: None | str | list[str] = None,
    ) -> dict:
        if keypath is None:
            keypaths_wanted = self._all_data_keypaths

        elif type(keypath) == str:
            keypaths_wanted = [keypath]

        else:
            keypaths_wanted = keypath

        for kp in keypaths_wanted:
            yield (
                kp,
                self.data[kp],
                self._main_parsers[kp][TAG_PARSER]
            )








# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# What I test.
    TEST_WANTED = [
        1, # Only project.
        # 2, # Only atoc.
    ]

# Let's go.
    from pprint import pprint

    projdir = Path(__file__).parent

    while projdir.name != 'for-dev':
        projdir = projdir.parent

# Only project.
    if 1 in TEST_WANTED:
        mydir = projdir / 'aboutmeta'

        amdata = AMData.new_instance(
            flavour = TAG_IT_PROJECT,
            parent  = mydir,
        )

        amdata.build()

        print(amdata.data.to_json(indent = 4))

        print()
        print(f'All keypaths: {amdata._all_data_keypaths}')

        first_data = amdata.data[amdata._all_data_keypaths[0]]

        print()
        print(f'1st data: {first_data}')
        print(f'    repr: {first_data!r}')

        new_yaml_code = amdata.standardize()

        print()
        print(amdata.std_data.to_json(indent = 4))


# Only atoc.
    if 2 in TEST_WANTED:
        mydir = (
              projdir
            / 'aboutmeta' / 'contribute' / 'api'
            / 'parser' / 'readme'
        )

        amdata = AMData.new_instance(
            flavour = TAG_ATOC,
            parent  = mydir,
        )

        amdata.build()

        print(amdata.data.to_json(indent = 4))

        print()
        print(amdata._all_data_keypaths)
