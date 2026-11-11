#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.parser.acronym import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/acronym.py'

from hypothesis import (
    given,
    strategies as st
)


# ------------------ #
# -- BACK TO SPEC -- #
# ------------------ #

@given(
    yaml_data = st.sampled_from([
        "[about::@] [meta]data",
    ]),
)
def test_back_2_spec(yaml_data: str) -> None:
    assert write(parse(yaml_data)) == yaml_data