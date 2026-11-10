#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/ymdate.py'


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
#     data : date provided in the \yaml file.
#
#     :return: ''datetime.date'' instance representing the date.
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
#     data : ''datetime.date'' object.
#
#     :return: ''"%Y-%m-%d"'' format value of the ''datetime.date''
#              object.
###
def write(data: datetime.date) -> str:
    return data.strftime('%Y-%m-%d')
