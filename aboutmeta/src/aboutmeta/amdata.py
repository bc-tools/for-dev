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
    def build(self) -> dict:
        self._yaml_raw_data = safe_load(
            self.yaml_file.read_text()
        )

# Validation de la structure initiale
        block_names_used = set(self._yaml_raw_data)

        if not self._mandatory_block_names <= block_names_used:
            raise ValueError('miising main blocks')

# Trvaille sur chque main blcok
        data = dict()

        for k, v in self._yaml_raw_data.items():
            self._pre_keypath = [k]

            specs = self._flavour_specs[k]

            self._parsers = specs[TAG_BLOCK_PARSERS]
            self._status  = specs[TAG_BLOCK_STATUS]
            self._alts    = specs[TAG_BLOCK_ALTS]

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
            raise ValueError('UNSUPPORTED_TYPE')

###
# XXXX
###
    def _recu_build_list(
        self,
        raw_data: list,
    ) -> dict:
        TODO

###
# XXXX
###
    def _recu_build_dict(
        self,
        raw_data: dict,
    ) -> dict:
        data = dict()

# TODO Good use of keys.

# Let's parse...
        for key, val in raw_data.items():
            print('.'.join(self._pre_keypath + [key]))



# Nothing left todo.
        return data


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
