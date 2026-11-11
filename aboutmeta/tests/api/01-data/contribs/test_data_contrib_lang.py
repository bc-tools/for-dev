#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.data.lang import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/data/code/lang.py'

from random import Random

from hypothesis import (
    given,
    settings, # Cf coverage tests.
    strategies as st
)

import pytest


# ---------------- #
# -- LEGAL SPEC -- #
# ---------------- #

@settings(deadline = None) # Cf coverage tests.
@given(
    full_data = st.sampled_from([
        (
            'fr', 'fr-FR',
            'French', 'France',
        ),
        (
            'en', 'en-US',
            'English', 'United States',
        ),
        (
            'en-GB', 'en-GB',
            'English', 'United Kingdom',
        ),
    ]),
)
def test_legal_spec(
    full_data: tuple[str, str, str, str]
) -> None:
    yaml_data, std_id, name, territory = full_data

    mydata = Lang(std_id = yaml_data)

    assert mydata.std_id == std_id
    assert mydata.name == name
    assert mydata.territory == territory


# ------------------------------- #
# -- LEGAL WEIRD LETTER CASING -- #
# ------------------------------- #

@given(
    std_id = st.sampled_from([
        'fr-BE',
        'es-ES',
        'en-US',
    ]),
    rnd = st.randoms(),
)
def test_weird_letter_casing(
    std_id: str,
    rnd   : Random
) -> None:
    weird_id = ''.join([
        rnd.choice([c.lower(), c.upper()])
        for c in std_id
    ])

    for sep in '-_':
        weird_id = weird_id.replace('-', sep)

    weird_data = Lang(std_id = weird_id)

    assert weird_data.std_id == std_id


# ------------------ #
# -- UNKNOWN LANG -- #
# ------------------ #

@given(
    yaml_data = st.sampled_from([
        'XXX',
    ]),
)
def test_unknown_lang(yaml_data: str) -> None:
    with pytest.raises(ValueError) as e:
        Lang(std_id = yaml_data)


# --------------------- #
# -- ILLEGAL LANG ID -- #
# --------------------- #

@given(
    yaml_data = st.sampled_from([
        'X.X',
    ]),
)
def test_illegal_lang_ID(yaml_data: str) -> None:
    with pytest.raises(ParsingError) as e:
        Lang(std_id = yaml_data)


# ----------------------- #
# -- ILLEGAL DATA TYPE -- #
# ----------------------- #

@given(
    yaml_data = st.sampled_from([
        None,
        123,
    ]),
)
def test_illegal_data_type(yaml_data : object) -> None:
    with pytest.raises(TypeError) as e:
        Lang(std_id = yaml_data)