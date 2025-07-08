#!/usr/bin/env python3

import aboutmeta


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

from datetime import datetime


### TODO
# prototype::
#     content : XXX
#
#     :return: XXX
###
def parser(content: str) -> datetime.date:
    d = datetime.strptime(
        content,
        "%Y-%m-%d"
    ).date()

    return d


# ----------------------------- #
# -- HUMAN TESTS (MANDATORY) -- #
# ----------------------------- #

if __name__ == "__main__":
    for onedate in [
        "2025-06-27",
        # "2.3",          # Test of an exception.
        # "2025-02-30",   # Test of an exception.
    ]:
        d = parser(onedate)

        print()
        print(f'--- ({onedate})')

        print(repr(d))

        print(d.year)
        print(d.month)
        print(d.day)

    print()
