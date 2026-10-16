#!/usr/bin/env python3

import re

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ---------- #
# -- DATA -- #
# ---------- #

PATTERN_UNIX_NAME = re.compile(r'^[a-z_][a-z0-9_-]*$')


###
# prototype::
#     name : a Unix-style name that only uses lowercase letters,
#            digits, underscores, and hyphens, and cannot start
#            with a digit or a hyphen.
###
class UnixName(DataManager):
    name: str

###
# prototype::
#     :action: mandatory validation of the Unix name.
###
    def __post_init__(self):
        if not PATTERN_UNIX_NAME.match(self.name):
            raise ParsingError(f'Unvalid Unix name "{name}".')


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    for yaml_data in [
        "_abc-cde123",
    ]:
        mydata = Unixname(name = yaml_data)

        print()
        print(f"{yaml_data = }")
        print(f"{mydata    = }")

# BAD
    # exit()

    print("\n------------\n")

    print("-- BAD CASES --")

    for yaml_data in [
        "-hyphen-pb",
        "CasePB",
        "123-digits-pb",
    ]:
        print()
        print(f"{yaml_data = }")

        try:
            Unixname(name = yaml_data)

        except Exception as e:
            print(type(e).__name__, ':', e)

            notes = getattr(e, "__notes__", [])

            for i, n in enumerate(notes, start = 1):
                print(f'[{i}]. {n}')
