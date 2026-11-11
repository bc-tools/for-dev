#!/usr/bin/env python3

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.parser.about_path import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/about_path.py'

from hypothesis import (
    given,
    strategies as st
)

import              pytest
from pathlib import Path

from aboutmeta.core.temp_dirtree import *


# --------------- #
# -- Moke data -- #
# --------------- #

mydirview = """
- readme.md
- script-10.py
- script-02.py
- library:
  - main.py
  - core:
    - readme.md
    - tool.py
    """

fake_sub_postprod_files = [
    'I.am',
    'danse.le',
    'Mi.a',
]

class MokeAMData:
    @classmethod
    def new_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __init__(
        self,
        flavour: str,
        parent : Path,
    ):
        self.flavour = flavour
        self.parent  = parent

    def build(self):
# Mock system does not provide build capabilities.
        ...

    def postprod(
        self,
        keypath: str | list[str] = '',
    ) -> object:
        return {
            TAG_POSTPROD_ABOUT_PATH_FILES: [
                self.parent / p
                for p in fake_sub_postprod_files
            ]
        }


# ------------------ #
# -- Back to spec -- #
# ------------------ #

@given(
    yaml_data = st.sampled_from([
        Path(__file__).name,
        {'r-glob': "*.py"},
        {'r-regex': r".*\.py"},
    ]),
)
def test_back_2_spec(yaml_data: str) -> None:
    moke_amdata = MokeAMData(
        flavour = 'fake-flavour',
        parent  = Path('fake-dir'),
    )

    assert write(
        parse(
            amdata = moke_amdata,
            data   = yaml_data
        )
    ) == yaml_data


# --------------- #
# -- Post prod -- #
# --------------- #

@given(
    full_data = st.sampled_from([
        (
            ['readme.md'],
            ['readme.md'],
        ),
        (
            [
                {'rg': '*.py'},
            ],
            [
                'library/core/tool.py',
                'library/main.py',
                'script-02.py',
                'script-10.py',
            ],
        ),
        (
            [
                {'g': '*.py'},
                {'g': '*/*.py'},
            ],
            [
                'script-02.py',
                'script-10.py',
                'library/main.py',
            ],
        ),
        (
            [
                {'g': '*.py'},
                'structure/',
            ],
            [
                'script-02.py',
                'script-10.py',
            ] + [
                f'structure/{n}'
                for n in fake_sub_postprod_files
            ],
        ),
    ]),
)
def test_post_prod(full_data: str) -> None:
    yaml_data, paths_wanted = full_data

    with temp_dirtree(mydirview) as tempdir:
        moke_amdata = MokeAMData(
            flavour = 'fake-flavour',
            parent  = tempdir,
        )

        tocpath_list = [
            parse(
                amdata = moke_amdata,
                data   = y
            )
            for y in yaml_data
        ]

        paths_found = [
            str(p.relative_to(tempdir))
            for _, paths in postprod(
                amdata = moke_amdata,
                data   = tocpath_list,
            ).items()  # Funny Python!
            for p in paths
        ]

    assert paths_found == paths_wanted