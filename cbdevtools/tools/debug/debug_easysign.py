#!/usr/bin/env python3

LOCAL_TEST = False
LOCAL_TEST = True


from pprint import pprint


if LOCAL_TEST:
    from cbdevtools import *


# ! -- DEBUGGING -- ! #
# Clear the terminal.
print("\033c", end = "")
# ! -- DEBUGGING -- ! #


# ------------------------------------ #
# -- MODULES IMPORTED FROM SOURCES! -- #
# ------------------------------------ #

if LOCAL_TEST:
    MODULE_DIR = addfindsrc(
        file    = __file__,
        project = 'cbdevtools',
    )


# -------------- #
# -- LET'S GO -- #
# -------------- #

if LOCAL_TEST:
    from src.easysign import easysign

else:
    from cbdevtools.easysign import easysign


class Test:
    def nothing(self):
        ...
    def noparam(self) -> str:
        ...
    def partialsign(self, a: str, b):
        ...
    def paramOK(self, a, b: bool = True) -> str:
        ...

mytest = Test()

for name in [
    "nothing",
    "noparam",
    "partialsign",
    "paramOK",
]:
    print(f"easysign(mytest.{name})")
    pprint(
        easysign(
            mytest.__getattribute__(name)
        )
    )
    print()

# exit()


def funcOK(a: int, b: int = 1) -> str:
    ...

for f in [
    funcOK,
]:
    print(f"easysign({funcOK.__name__})")
    pprint(easysign(funcOK))
    print()

exit()


print(easysign(1))
