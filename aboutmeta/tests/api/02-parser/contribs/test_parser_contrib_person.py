#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.parser.person import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/person.py'

# We just need some basic interface tests, because we have already
# tested the ''Person'' class.

from hypothesis import (
    given,
    strategies as st
)


# ------------------ #
# -- BACK TO SPEC -- #
# ------------------ #

@given(
    yaml_data = st.sampled_from([
        "{Mc} Someone",
        "Marie-Lise, {Mc} Someone",
        "Alice, Marie-Lise, {Mc} Someone",
        "Alice, Marie-Lise, {Mc} Someone [e.mail@provided.by]",
        "Alice, Marie-Lise, {Mc} Someone [e.mail@provided.by] (My address)",
    ]),
)
def test_back_2_spec(yaml_data: str) -> None:
    assert write(parse(yaml_data)) == yaml_data