#!/usr/bin/env python3

from datetime import datetime

from aboutmeta.core.errors import ParsingError


# ------------ #
# -- PARSER -- #
# ------------ #

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
                  "Format used."
                "\n  %Y = 4-digit year"
                "\n  %m = 2-digit month"
                "\n  %d = 2-digit day"
            )

        raise e

    return date


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    for onedate in [
        "2025-06-27",
    ]:
        print()

        date_data = parse(onedate)

        print(f'{onedate         = }')
        print( f"repr(date_data) = {date_data!r}")
        print(f"{date_data.year  = }")
        print(f"{date_data.month = }")
        print(f"{date_data.day   = }")


# BAD
    # exit()

    print("\n------------\n")

    print("-- BAD CASES --")

    for onedate in [
        "2.3",
        "2/3/2025",
        "2025-02-30",
    ]:
        print()

        print(f'{onedate = }')

        try:
            parse(onedate)

        except Exception as e:
            print(type(e).__name__, ':', e)

            notes = getattr(e, "__notes__", [])

            for i, n in enumerate(notes, start = 1):
                print(f'[{i}]. {n}')
