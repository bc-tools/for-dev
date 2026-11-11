#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.data.url import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/data/code/url.py'

from hypothesis import (
    given,
    strategies as st
)

import pytest


# --------------- #
# -- LEGAL URL -- #
# --------------- #

@given(
    yaml_data = st.sampled_from([
        'HTTPS://QwAnT.com',
        'qwant.com',
        'HTTP://Example.COM/Mon Dôssier/Fichier Testé.html',
    ]),
)
def test_legal_URL(yaml_data):
    mydata = URL(url = yaml_data)

    assert mydata.url == yaml_data


# -------------------- #
# -- NORMALIZED URL -- #
# -------------------- #

@given(
    full_data = st.sampled_from([
        (
            'HTTPS://QwAnT.com',
            'https://qwant.com'
        ),
        (
            'qwant.com',
            'qwant.com'
        ),
        (
            'HTTP://Example.COM/Mon Dôssier/Fichier Testé.html',
            'http://example.com/Mon%20D%C3%B4ssier/Fichier%20Test%C3%A9.html'
        ),
    ]),
)
def test_normalized_URL(full_data):
    yaml_data, std_url = full_data

    mydata = URL(url = yaml_data)
    mydata.normalize()

    assert mydata.url == std_url


# ----------------------- #
# -- ILLEGAL DATA TYPE -- #
# ----------------------- #

@given(
    yaml_data = st.sampled_from([
        None,
        123,
    ]),
)
def test_illegal_data_type(yaml_data):
    with pytest.raises(TypeError) as e:
        URL(url = yaml_data)