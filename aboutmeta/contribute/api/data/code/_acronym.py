#!/usr/bin/env python3

from dataclasses import dataclass

from aboutmeta.core.data_manager import DataManager


# ------------------- #
# -- MY DATA CLASS -- #
# ------------------- #

###
# prototype::
#     std : xxx
#     xxx  : yyyy
###
@dataclass(frozen = True)
class MyDataClass(DataManager):
    xxx : list[str]
    surname    : tuple[str | None, str]
    email      : str | None
    affiliation: str | None

###
# prototype::
#     :return: ???
###
    def normalized(self) -> str:
        ...


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print("----------")
    print("GOOD CASES")
    print("----------")

    ...

# BAD
    exit()

    print()
    print("---------")
    print("BAD CASES")
    print("---------")

    ...
