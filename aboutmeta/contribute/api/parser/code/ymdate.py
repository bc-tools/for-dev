#!/usr/bin/env python3

###
# An ''YMD'' date follows English format "YYYY-MM-DD" like
# "2025-10-31".
###


from datetime import datetime

from aboutmeta.core.errors import ParsingError


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : the date provided in the \yaml file, but stripped.
#
#     :return: an instance of the ''datetime.date'' class
#              representing the date.
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


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''datetime.date'' object.
#
#     :return: the \std \yaml version of the ''datetime.date''
#              object using the format ''"%Y-%m-%d"''.
###
def write(data: datetime.date) -> str:
    return data.strftime('%Y-%m-%d')


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print()
    print("-- GOOD CASES --")

    for yaml_data in [
        "2025-06-27",
    ]:
        data_parsed = parse(yaml_data)

        print()
        print('~~~')

        print()
        print(f"{yaml_data          = }")
        print(f"{data_parsed        = }")
        print(f"{write(data_parsed) = }")

        print()
        print(f"{data_parsed.year  = }")
        print(f"{data_parsed.month = }")
        print(f"{data_parsed.day   = }")

# BAD
    # exit()

    print()
    print("-- BAD CASES --")

    for yaml_data in [
        "2.3",
        "2/3/2025",
        "2025-02-30",
    ]:
        print()
        print('~~~')
        print()

        print(f'{yaml_data = }')

        try:
            parse(yaml_data)

        except Exception as e:
            print(type(e).__name__, ':', e)

            notes = getattr(e, "__notes__", [])

            for i, n in enumerate(notes, start = 1):
                print(f'[{i}]. {n}')
