#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.data.errors import ParsingError

from datetime import datetime


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     data : the date provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''datetime.date'' to work
#              easily with the date.
###
def parser(data: str) -> datetime.date:
    try:
        date = datetime.strptime(
            data,
            "%Y-%m-%d"
        ).date()

    except ValueError as e:
        raise ParsingError(e)

    return date


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

        date_data = parser(onedate)

        print(repr(date_data))

        print(date_data.year)
        print(date_data.month)
        print(date_data.day)

    print()

# Corrupted data.
    onedate = "2.3"
    onedate = "2025-02-30"
    onedate = "2/3/2025"

    print(f'--- ({onedate}) --> CORRUPTED!')

    date_data = parser(onedate)
