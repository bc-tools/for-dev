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


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

# dev:
    yaml_data   = "2025-06-27"
    data_parsed = parse(yaml_data)

    print('---')
    print(f"{yaml_data          = }")
    print(f"{data_parsed        = }")
    print(f"{data_parsed.year   = }")
    print(f"{data_parsed.month  = }")
    print(f"{data_parsed.day    = }")
    print(f"{write(data_parsed) = }")
# :dev

# -- Data - Illegal spec -- #
    @given(
        yaml_data = st.sampled_from([
            "2.3",
            "2/3/2025",
            "2025-02-30",
        ]),
    )
    def test_illegal_spec(yaml_data: str) -> None:
        with pytest.raises(ParsingError) as e:
            parse(yaml_data)

# dev:
        print('---')
        print(f'{yaml_data = }')
        print(e)
# :dev

    test_illegal_spec()

# -- Data - Illegal data type -- #
    @given(
        yaml_data = st.sampled_from([
            None,
            123,
        ]),
    )
    def test_illegal_data_type(yaml_data: object) -> None:
        with pytest.raises(TypeError) as e:
            parse(yaml_data)

# dev:
        print('---')
        print(f'{yaml_data = }')
        print(e)
# :dev

    test_illegal_data_type()

# -- Parser - Back to spec -- #
    @given(
        yaml_data = st.sampled_from([
            "2026-11-08",
        ]),
    )
    def test_back_2_spec(yaml_data: str) -> None:
        assert write(parse(yaml_data)) == yaml_data

    test_back_2_spec()
