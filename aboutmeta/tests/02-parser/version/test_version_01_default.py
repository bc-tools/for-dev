#!/usr/bin/env python3

import pytest

from aboutmeta.parser.version.default import parser


# ----------- #
# -- LEGAL -- #
# ----------- #

def test_parser_version_default_OK():
    for major, minor, patch, prerelease, build in [
        (2, 3, 4, "beta.1", "build.5"),
        (2, 3, 4, "beta.1", ""       ),
        (2, 3, 4, ""      , ""       ),
    ]:
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

        assert major      == version_data.major, f"version tested: {nbver}"
        assert minor      == version_data.minor, f"version tested: {nbver}"
        assert patch      == version_data.patch, f"version tested: {nbver}"
        assert prerelease == version_data.prerelease, f"version tested: {nbver}"
        assert build      == version_data.build, f"version tested: {nbver}"


# ------------- #
# -- ILLEGAL -- #
# ------------- #

def test_parser_version_default_KO():
    for nbver in [
        "2.3",
        "2025-02-30"
    ]:
        with pytest.raises(ValueError):
            parser(nbver)
