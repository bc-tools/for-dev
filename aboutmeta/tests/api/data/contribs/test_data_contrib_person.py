#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.data.person import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/data/code/person.py'

from random import Random

from hypothesis import (
    given,
    strategies as st
)

import pytest


# ------------------- #
# -- Weird spacing -- #
# ------------------- #

@given(
    std_spec = st.sampled_from([
        'Alice, Marie-lise, {mc} Someone [e.mail@provided.by]',
    ]),
    rnd = st.randoms(),
)
def test_weird_spacing(
    std_spec: str,
    rnd     : Random
) -> None:
    weird_spec = ' '.join([
        p + ' '*rnd.randint(0,5)
        for p in std_spec.split(' ')
    ])

    weird_data = Person(spec = weird_spec)

    assert weird_data.spec == std_spec


# ----------------------------------- #
# -- Normalize weird letter casing -- #
# ----------------------------------- #

@given(
    std_spec = st.sampled_from([
        '{mc} Someone',
        'Alice, Marie-Lise, {mc} Someone',
        'Alice, Marie-Lise, {mc} Someone [e.mail@provided.by]',
    ]),
    rnd = st.randoms(),
)
def test_weird_letter_casing(
    std_spec: str,
    rnd     : Random
) -> None:
    def weirdcase(text):
        return ''.join([
        rnd.choice([c.lower(), c.upper()])
        for c in text.strip()
    ])

    if '[' in std_spec:
        before_email, _ , email = std_spec.partition('[')

        email = email[:-1]

        local_part, _ , domain_part = email.partition('@')

        before_email = weirdcase(before_email)
        domain_part  = weirdcase(domain_part)

        weird_spec = f'{before_email} [{local_part}@{domain_part}]'

    else:
        weird_spec = weirdcase(std_spec)

    weird_data = Person(spec = weird_spec)
    weird_data.normalize()

    assert weird_data.spec == std_spec, weird_data.spec


# ------------------ #
# -- Illegal spec -- #
# ------------------ #

@given(
    yaml_data = st.sampled_from([
        'Someone (My address) [e.mail@provided.by]',
        'Someone [e.mail@provided.by (My address)',
        'Someone [e.mail@provided.by] (My address',
    ]),
)
def test_illegal_spec(yaml_data: str) -> None:
    with pytest.raises(ParsingError) as e:
        Person(spec = yaml_data)


# ----------------------- #
# -- Illegal data type -- #
# ----------------------- #

@given(
    yaml_data = st.sampled_from([
        None,
        123,
    ]),
)
def test_illegal_data_type(yaml_data: object) -> None:
    with pytest.raises(TypeError) as e:
        Person(spec = yaml_data)