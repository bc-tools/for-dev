#!/usr/bin/env python3

# Code extracted from the maintained Python file
# aboutmeta/contribute/api/parser/code/date.py

###
# A date can only be given in the English format ''YYYY-MM-DD''
# like ''2025-07-15''.
###


from datetime import datetime

from aboutmeta.core.errors import ParsingError


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : the date provided in the \yaml file, but stripped.
#     :return: an instance of the ''datetime.date'' class.
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
#     :return: the standard \yaml version of the ''datetime.date''
#              object using the format `%Y-%m-%d`.
###
def write(data: datetime.date) -> str:
    return data.strftime('%Y-%m-%d')
