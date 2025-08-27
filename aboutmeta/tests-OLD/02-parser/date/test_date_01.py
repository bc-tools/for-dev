#!/usr/bin/env python3

import pytest

from aboutmeta.parser.date.default import parser


# ----------- #
# -- LEGAL -- #
# ----------- #

@pytest.mark.parametrize(
    "onedate",
    [
        "2025-06-27",
    ]
)
def test_parser_date_default_Y_M_D_OK(onedate):
    year, month, day = onedate.split('-')

    date_data = parser(onedate)

    assert date_data.year  == int(year)
    assert date_data.month == int(month)
    assert date_data.day   == int(day)


# ------------- #
# -- ILLEGAL -- #
# ------------- #

@pytest.mark.parametrize(
    "onedate",
    [
        "2.3",
        "2025-02-30",
    ]
)
def test_parser_date_default_KO(onedate):
    with pytest.raises(ValueError):
        parser(onedate)
