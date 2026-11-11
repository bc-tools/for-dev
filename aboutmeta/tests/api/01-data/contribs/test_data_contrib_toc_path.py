#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.data.toc_path import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/data/code/toc_path.py'

from hypothesis import (
    given,
    strategies as st
)

import pytest

from pathlib import Path

from aboutmeta.core.temp_dirtree import *

TAG_RAW        = 'raw'
TAG_GLOB       = 'glob'
TAG_GLOB_RECU  = 'r-glob'
TAG_REGEX      = 'regex'
TAG_REGEX_RECU = 'r-regex'


# --------------- #
# -- MOKE DATA -- #
# --------------- #

mydirview = """
- readme.md
- script-1.py
- script-02.py
- library:
  - main.py
  - core:
    - readme.md
    - tool.py
    """

mydirview = mydirview.strip()


# ---------------- #
# -- LEGAL SPEC -- #
# ---------------- #

@given(
    full_data = st.sampled_from([
        # Raw path.
        (
            TAG_RAW,
            'readme.md'
        ),
        # Glob patterns.
        (
            TAG_GLOB,
            {'glob': '*/*.md'}
        ),
        (
            TAG_GLOB,
            {'glob': r'*\[.md'}
        ),
        # Regex patterns.
        (
            TAG_REGEX,
            {'regex': r'.*\.md'}
        ),
    ]),
)
def test_legal_spec(
    full_data: tuple[str, str | dict[str, str]]
) -> None:
    kind, yaml_data = full_data

    with temp_dirtree(mydirview) as tempdir:
        mydata = TOCPath(
            spec   = yaml_data,
            parent = tempdir
        )

    assert mydata.kind == kind


# ------------------------------ #
# -- VALIDATION OF GOOD SPECS -- #
# ------------------------------ #

@given(
    yaml_data = st.sampled_from([
        # Raw path.
        'readme.md',
        # Glob patterns.
        {'glob': '*.md'},
        {'glob': '*.py'},
        {'rg': '*.py'},
        # Regex patterns.
        {'r': r'.*\.md'},
        {'rr': r'.*\.py'},
        {'r': r'[^/]*\.py'},
    ]),
)
def test_tocpath_validation(
    yaml_data: str | dict[str, str]
) -> None:
    with temp_dirtree(mydirview) as tempdir:
        mydata = TOCPath(
            spec   = yaml_data,
            parent = tempdir
        )

        mydata.validate()

        assert not mydata._errors_found


# ------------------ #
# -- ILLEGAL SPEC -- #
# ------------------ #

@given(
    yaml_data = st.sampled_from([
        # Glob patterns.
        {'g': '*.md', 'r': '*.md'},
        {'gob': '*.md'},
        {'g': r'*\.md]'},
        {'glob': '**/[a-z'},
        # Regex patterns.
        {'r': '(abc'},
    ]),
)
def test_illegal_spec(yaml_data: dict[str, str]) -> None:
    with pytest.raises(ParsingError) as e:
        TOCPath(
            spec   = yaml_data,
            parent = Path('')
        )


# ----------------------- #
# -- ILLEGAL DATA TYPE -- #
# ----------------------- #

@given(
    yaml_data = st.sampled_from([
        None,
        123,
        Path(__file__).name # For illegal parent type.
    ]),
)
def test_illegal_data_type(yaml_data: object) -> None:
    with pytest.raises(TypeError) as e:
        TOCPath(
            spec   = yaml_data,
            parent = None
        )


# -------------------- #
# -- PATH ITERATION -- #
# -------------------- #

@given(
    full_data = st.sampled_from([
        (
            {'g': '*.py'},
            ['script-02.py',
             'script-1.py',]
        ),
        (
            {'rg': '*.py'},
            ['script-02.py',
             'script-1.py',
             'library/main.py',
             'library/core/tool.py',]
        ),
    ]),
)
def test_path_iteration(
    full_data: tuple[dict[str, str], list[str]]
) -> None:
    yaml_data, paths = full_data

    with temp_dirtree(mydirview) as tempdir:
        mydata = TOCPath(
            spec   = yaml_data,
            parent = tempdir
        )

        paths_founds = [
            str(p.relative_to(tempdir))
            for p in mydata.path_iter()
        ]

    assert paths == paths_founds