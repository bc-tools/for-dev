#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.core.errors import ParsingError

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
def parse(data: str) -> datetime.date:
    try:
        date = datetime.strptime(data, "%Y-%m-%d").date()

    except ValueError as e:
        e = ParsingError(e)

        if '%Y' in str(e):
            e.add_note(
                "Expected format: %Y-%m-%d means "
                "something like '2025-03-02'."
            )
            e.add_note(
                  "  %Y = 4-digit year"
                "\n  %m = 2-digit month"
                "\n  %d = 2-digit day"
            )

        raise e

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

        date_data = parse(onedate)

        print(date_data)
        print(f"date_data = {date_data!r}")

        print(date_data.year)
        print(date_data.month)
        print(date_data.day)

    print()

# Corrupted data.
    # exit()

    onedate = "2.3"
    # onedate = "2025-02-30"
    # onedate = "2/3/2025"

    print(f'--- ({onedate}) --> CORRUPTED!')

    parse(onedate)
