#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.parser.acronym import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/acronym.py'

# We just need some basic interface tests, because we have
# already tested the ''Acronym'' class.

from hypothesis import (
    given,
    strategies as st
)


# ------------------ #
# -- Back to spec -- #
# ------------------ #

@given(
    yaml_data = st.sampled_from([
        "[about::@] [meta]data",
    ]),
)
def test_back_2_spec(yaml_data: str) -> None:
    assert write(parse(yaml_data)) == yaml_data