#!/usr/bin/env python3


# extract en mode cool : on veut juste un dict avec els cles des blocs et d'autres en plus ok
# extract(soft=False) pour mode strict

# postprod() : pour tous ces qu'i peut l'etre : résultat stocké dans un dict dédié

# posprod(keypath) : pour un sous jeu de donné ou une donné

from pathlib import Path

from benedict import benedict
from yaml     import safe_load

from aboutmeta.core.constants                 import *
from aboutmeta.specs.flavour.__ALL_FLAVOURS__ import *


###
# self.yaml_file
# self.data
# self.post_vals
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
# XXXX
###
    @property
    def flavour(self) -> str:
        return self._flavour

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
# XXXX
###
    @property
    def parent(self) -> str:
        return self._parent

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
#     :return: ''benedict'' version of the data found.
###
    def build(
        self,
        tolerent: bool = True
    ) -> dict:
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
# XXXX
###
    def _recu_build(
        self,
        raw_data: dict | list,
    ) -> dict:
        if isinstance(raw_data, list):
            return self._recu_build_list(raw_data)

        elif isinstance(raw_data, dict):
            return self._recu_build_dict(raw_data)

        else:
            _type   = type(raw_data).__name__
            keypath = self._msg_get_keypath()

            raise ValueError(
                f'Unsupported yaml content Python typed {_type!r}. '
                f'See key {keypath!r}.'
            )



###
# TODO
###
    def _recu_build_list(
        self,
        raw_data: list,
    ) -> list:
# Good data type?
        datatype = self._main_parsers[self._pre_keypath].get(
            TAG_DATATYPE,
            None
        )

        if datatype != TAG_LIST:
            raise ValueError(
                f'Block {self._msg_get_keypath()!r} does not '
                 'expect a list of data to parse.'
            )

        parser_module, use_post = self._get_current_parser_spec()

# Only strings allowed!
        if parser_module == str:
            data = []

            for rd in raw_data:
                if not type(raw_data) == str:
                    raise ValueError(
                        f'Block {self._msg_get_keypath()!r} only '
                         'accepts a string list.'
                    )

                data.append(rd)

# Specilized parsers will found wrong data types.
        else:
            data = [
                parser_module.parse(
                    amdata = self,
                    data   = rd
                )
                for rd in raw_data
            ]

# Nothing left todo.
        return data

###
# XXXX
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

# A value to parse (datatype captured before).
            else:
                parser_module, use_post = self._get_current_parser_spec()

                if parser_module == str:
                    new_val = val

                else:
                    new_val = parser_module.parse(val)

# All work has been done!
            data[key] = new_val

# Pop the key from the key path.
            self._pre_keypath.pop(-1)

# Nothing left todo.
        return data




###
# XXXX
###
    def _get_current_parser_spec(self):
        return (
            self._main_parsers[self._pre_keypath][TAG_PARSER],
            self._main_parsers[self._pre_keypath][TAG_USE_POST],
        )

###
# XXXX
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
# XXXX
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
# XXXX
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
# XXXX
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
# XXXX
###
    def _msg_get_keypath(
        self,
        key: str = ''
    ):
        keypath = '.'.join(self._pre_keypath)

        if key:
            keypath += f'.{key}'

        return keypath

###
# XXXX
###
    def _msg_list_names(
        self,
        names: set[str],
        sep  : str = ', '
    ) -> (str, str):
        list_names = sep.join([
            f'{n!r}'
            for n in sorted(names)
        ])

        plurial = 's' if sep in list_names else ''

        return plurial, list_names






###
# XXXX
###
    def postprod(
        self,
        keypath: str | list[str] = '',
    ) -> dict:
        ...









# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from pprint import pprint

    projdir = Path(__file__).parent

    while projdir.name != 'for-dev':
        projdir = projdir.parent

    projdir /= 'aboutmeta'

    amdata = AMData.new_instance(
        flavour = TAG_IT_PROJECT,
        parent  = projdir,
    )

    amdata.build()

    print(amdata.data.to_json(indent = 4))
    print()
    print(amdata.data)
