#!/usr/bin/env python3

import pytest

from aboutmeta.parser.tocpath.default import parser, Path



# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_FILE = Path(__file__)
THIS_DIR  = THIS_FILE.parent

TEST_DIR_NAME = THIS_DIR.name

DATA_DIR    = THIS_DIR.parent.parent / "data"
OK_DATA_DIR = DATA_DIR / "OK" / TEST_DIR_NAME
KO_DATA_DIR = DATA_DIR / "KO" / TEST_DIR_NAME


# ----------- #
# -- LEGAL -- #
# ----------- #

@pytest.mark.parametrize(
    (
        "folder",
        "data",
        "kind",
        "relpaths",
    ),
    [
        (
            '01-basic',
            '01.md',
            'files',
            ['01.md']
        ),
        (
            '01-basic',
            '02/',
            'about',
            '02/about.yaml'
        ),
        (
            '01-basic',
            {'glob': "02/*.md"},
            'files',
            [
                '02/02-a.md',
                '02/02-b.md',
            ]
        ),
        (
            '01-basic',
            {'glob': "04-rev/*.md"},
            'files',
            [
                '04-rev/04-a.md',
                '04-rev/04-b.md',
                '04-rev/04-c.md',
            ]
        ),
        (
            '01-basic',
            {'regex': r".*-rev.*\.md"},
            'files',
            [
                '04-rev.md',
            ]
        ),
        (
            '01-basic',
            {'r-regex': r".*-rev.*\.md"},
            'files',
            [
                '04-rev.md',
                '04-rev/04-a.md',
                '04-rev/04-b.md',
                '04-rev/04-c.md',
            ]
        ),
    ]
)
def test_parser_tocpath_default_OK(
    folder,
    data,
    kind,
    relpaths
):
    folder = OK_DATA_DIR / folder

    tp_found = parser(
        parent = folder,
        data   = data
    )

    if kind == 'about':
        paths = folder / relpaths

    else:
        paths = [
            folder / p
            for p in relpaths
        ]

    assert tp_found.kind  == kind
    assert tp_found.paths == paths


# ------------- #
# -- ILLEGAL -- #
# ------------- #

def test_parser_tocpath_default_regex_KO():
    with pytest.raises(
        ValueError,
        match = "REGEX ERROR"
    ):
        parser(
            parent = "",
            data   = {'regex': r".*(K"}
        )


@pytest.mark.parametrize(
    (
        "data",
        "match_wanted"
    ),
    [
        (
            [1, 2],
            "dict expected"
        ),
        (
            {'1': 2, '3': 4},
            "single key expected"
        ),
        (
            {'glb': "*.md"},
            "illegal pattern kind"
        ),
    ]
)
def test_parser_tocpath_default_data_KO(
    data,
    match_wanted
):
    with pytest.raises(
        ValueError,
        match = match_wanted
    ):
        parser(
            parent = "",
            data   = data
        )


@pytest.mark.parametrize(
    (
        "folder",
        "data",
        "match_wanted"
    ),
    [
        (
            '01-basic',
            "abc.tex",
            "inexistant file"
        ),
        (
            '01-basic',
            "abc-TeX/",
            "inexistant folder"
        ),
        (
            '01-basic',
            "../",
            "missing sub ''about.yaml'' file"
        ),
        (
            '01-basic',
            {'glob': "*.tex"},
            "no files found"
        ),
        (
            '01-basic',
            {'g': "*.tex"},
            "no files found"
        ),
        (
            '01-basic',
            {'r': ".*\.tex"},
            "no files found"
        ),
    ]
)
def test_parser_tocpath_default_missing_files_KO(
    folder,
    data,
    match_wanted
):
    with pytest.raises(
        ValueError,
        match = match_wanted
    ):
        parser(
            parent = OK_DATA_DIR / folder,
            data   = data
        )
