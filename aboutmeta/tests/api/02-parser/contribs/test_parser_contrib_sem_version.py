#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.parser.sem_version import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/sem_version.py'

from hypothesis import (
    given,
    strategies as st
)

import pytest


# ------------------------- #
# -- DATA - ILLEGAL SPEC -- #
# ------------------------- #

@given(
    yaml_data = st.sampled_from([
        "2.3",
        "2-3-2025",
    ]),
)
def test_illegal_spec(yaml_data: str) -> None:
    with pytest.raises(ParsingError) as e:
        parse(yaml_data)


# ------------------------------ #
# -- DATA - ILLEGAL DATA TYPE -- #
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
# -- PARSER - BACK TO SPEC -- #
# --------------------------- #

@given(
    yaml_data = st.sampled_from([
        "4.5.6",
        "2.3.4-beta.1",
        "1.2.3-beta.4+build.5",
    ]),
)
def test_back_2_spec(yaml_data: str) -> None:
    assert write(parse(yaml_data)) == yaml_data