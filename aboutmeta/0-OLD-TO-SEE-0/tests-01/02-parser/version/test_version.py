#!/usr/bin/env python3

import pytest

from aboutmeta.parser.version.default import parser


# ----------- #
# -- LEGAL -- #
# ----------- #

@pytest.mark.parametrize(
    (
        "major",
        "minor",
        "patch",
        "prerelease",
        "build"
    ),
    [
        (2, 3, 4, "beta.1", "build.5"),
        (2, 3, 4, "beta.1", ""       ),
        (2, 3, 4, ""      , ""       ),
    ]
)
def test_parser_version_default_OK(
    major,
    minor,
    patch,
    prerelease,
    build
):
    nbver = f"{major}.{minor}.{patch}"

    if prerelease:
        nbver += f"-{prerelease}"

    else:
        prerelease = None

    if build:
        nbver += f"+{build}"

    else:
        build = None

    version_data = parser(nbver)

    assert major      == version_data.major
    assert minor      == version_data.minor
    assert patch      == version_data.patch
    assert prerelease == version_data.prerelease
    assert build      == version_data.build


# ------------- #
# -- ILLEGAL -- #
# ------------- #

@pytest.mark.parametrize(
    "nbver",
    [
        "2.3",
        "2025-02-30"
    ]
)
def test_parser_version_default_KO(nbver):
    with pytest.raises(ValueError):
        parser(nbver)
