#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/data/code/acronym.py'


from random import Random

from hypothesis import (
    given,
    strategies as st
)

import pytest


# ---------------- #
# -- Legal spec -- #
# ---------------- #

@given(
    full_data = st.sampled_from([
        (
            '[about] [meta]data',
            'aboutmeta',
            'about metadata'
        ),
        (
            '[about::@-] [meta::met-@]data',
            '@-met-@',
            'about metadata'
        ),
    ]),
)
def test_legal_spec(
    full_data: tuple[str, str, str]
) -> None:
    yaml_data, short, desc = full_data

    mydata = Acronym(spec = yaml_data)

    assert mydata.spec == yaml_data
    assert mydata.short == short
    assert mydata.desc == desc


# ------------------- #
# -- Weird spacing -- #
# ------------------- #

@given(
    std_spec = st.sampled_from([
        '[about] [meta]data',
        '[about::@-] [meta::met-@]data',
    ]),
    rnd = st.randoms(),
)
def test_weird_spacing(
    std_spec: str,
    rnd     : Random
) -> None:
    weird_spec = std_spec

    for old in [
        '[{space}',
        '{space}]',
        '{space}::',
        '::{space}',
    ]:
        new = old.format(space = ' ' * rnd.randint(1, 5))

        weird_spec = weird_spec.replace(
            old.replace('{space}', ''),
            new
        )

    weird_data = Acronym(spec = weird_spec)

    assert weird_data.spec == std_spec


# ------------------ #
# -- Illegal spec -- #
# ------------------ #

@given(
    yaml_data = st.sampled_from([
        'about metadata',
        '[about [meta]data',
        '[about] meta]data',
        '[about metadata',
        'about meta]data',
    ]),
)
def test_illegal_spec(yaml_data: str) -> None:
    with pytest.raises(ParsingError) as e:
        Acronym(spec = yaml_data)


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
        Acronym(spec = yaml_data)


