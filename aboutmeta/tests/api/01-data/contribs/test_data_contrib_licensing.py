#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.data.licensing import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/data/code/licensing.py'

from random import Random

from hypothesis import (
    given,
    strategies as st
)

import pytest


# ------------------------------ #
# -- LEGAL WEIRD LICENSE CODE -- #
# ------------------------------ #

@given(
    std_spdx_id = st.sampled_from([
        'GPL-3.0-only',
        'CC-BY-NC-4.0',
    ]),
    rnd = st.randoms(),
)
def test_legal_weird_license_code(
    std_spdx_id: str,
    rnd        : Random
) -> None:
    weird_spdx_id = ''.join([
        rnd.choice([c.lower(), c.upper()])
        for c in std_spdx_id
    ])

    weird_spdx_id = ' '.join([
        p + ' '*rnd.randint(0,5) + '-'*rnd.randint(0, 1)
        for p in weird_spdx_id.split('-')
    ])

    if weird_spdx_id[-1] == '-':
        weird_spdx_id = weird_spdx_id[:-1]

    weird_data = Licensing(spdx_id = weird_spdx_id)

    assert weird_data.spdx_id == std_spdx_id


# -------------------------- #
# -- ILLEGAL LICENSE CODE -- #
# -------------------------- #

@given(
    yaml_data = st.sampled_from([
        'gpl-3.0-only-',
        'gpl 3..0 only',
        'gpl 3.0+',
        'gpl',
        'cc nc',
        'cc',
        '',
    ]),
)
def test_illegal_license_code(yaml_data: str) -> None:
    with pytest.raises(ValueError) as e:
        Licensing(spdx_id = yaml_data)


# ----------------------- #
# -- ILLEGAL DATA TYPE -- #
# ----------------------- #

@given(
    yaml_data = st.sampled_from([
        None,
        123,
    ]),
)
def test_illegal_data_type(yaml_data: object) -> None:
    with pytest.raises(TypeError) as e:
        Licensing(spdx_id = yaml_data)