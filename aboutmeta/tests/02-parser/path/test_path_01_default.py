#!/usr/bin/env python3

import pytest

from aboutmeta.parser.path.default import parser, Path



# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_FILE = Path(__file__)
THIS_DIR  = THIS_FILE.parent


# ----------- #
# -- LEGAL -- #
# ----------- #

@pytest.mark.parametrize(
    ("isdir", "pdir", "path", "abspath"),
    [
        (
            False,
            THIS_DIR,
            str(THIS_FILE.name),
            THIS_FILE
        ),
        (
            True,
            THIS_DIR,
            "./",
            THIS_DIR
        ),
        (
            True,
            THIS_DIR,
            "../../",
            THIS_DIR.parent.parent
        ),
    ]
)
def test_parser_path_default_OK(isdir, pdir, path, abspath):
    abspath_found = parser(pdir, path)

    assert isdir   == abspath_found.is_dir()
    assert abspath == abspath_found


# ------------- #
# -- ILLEGAL -- #
# ------------- #

@pytest.mark.parametrize(
    ("pdir", "path"),
    [
        (THIS_DIR, "_X-x-X_"),
        (THIS_DIR, "_X-x-X_/"),
    ]
)
def test_parser_path_default_KO(pdir, path):
    with pytest.raises(ValueError):
        parser(pdir, path)
