#!/usr/bin/env python3

import pytest

from aboutmeta.parser.date.default import parser


# ----------- #
# -- LEGAL -- #
# ----------- #

def test_parser_date_default_OK():
    for year, month, day in [
        ("2025", "06", "27"),
    ]:
        onedate   = f"{year}-{month}-{day}"
        date_data = parser(onedate)

        assert date_data.year  == int(year) , f"date tested: {ondeate}"
        assert date_data.month == int(month), f"date tested: {ondeate}"
        assert date_data.day   == int(day)  , f"date tested: {ondeate}"


# ------------- #
# -- ILLEGAL -- #
# ------------- #

def test_parser_date_default_KO():
    for onedate in [
        "2.3",
        "2025-02-30"
    ]:
        with pytest.raises(ValueError):
            parser(onedate)
