#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.parser.ymdate import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/ymdate.py'

from hypothesis import (
    given,
    strategies as st
)

import pytest


# ------------------------- #
# -- Data - Illegal spec -- #
# ------------------------- #

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


# ------------------------------ #
# -- Data - Illegal data type -- #
# ------------------------------ #

@given(
    yaml_data = st.sampled_from([
        None,
        123,
    ]),
)
def test_illegal_data_type(yaml_data: object) -> None:
    with pytest.raises(TypeError) as e:
        parse(yaml_data)


# --------------------------- #
# -- Parser - Back to spec -- #
# --------------------------- #

@given(
    yaml_data = st.sampled_from([
        "2026-11-08",
    ]),
)
def test_back_2_spec(yaml_data: str) -> None:
    assert write(parse(yaml_data)) == yaml_data