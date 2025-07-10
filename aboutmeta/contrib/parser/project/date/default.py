#!/usr/bin/env python3

import aboutmeta


# ------------- #
# -- IMPORTS -- #
# ------------- #

from datetime import datetime


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : the date provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''datetime.date'' to work
#              easily with the date.
###
def parser(content: str) -> datetime.date:
    d = datetime.strptime(
        content,
        "%Y-%m-%d"
    ).date()

    return d


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
# Working examples.
    for onedate in [
        "2025-06-27",
    ]:
        print()
        print(f'--- ({onedate})')

        d = parser(onedate)

        print(repr(d))

        print(d.year)
        print(d.month)
        print(d.day)

    print()

# Corrupted data.
    onedate = "2.3"
    onedate = "2025-02-30"

    print(f'--- ({onedate}) --> CORRUPTED!')

    d = parser(onedate)
