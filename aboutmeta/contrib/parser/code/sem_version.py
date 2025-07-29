#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.data.errors import ParsingError

from semver import (
    Version,
    VersionInfo,
)


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     data : the \nbver provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''semver.Version'' to work
#              easily with the number version.
###
def parser(data: str) -> Version:
    try:
        version = VersionInfo.parse(data)

    except ValueError as e:
        raise ParsingError(e)

    return version


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
# Working examples.
    for nbver in [
        "1.2.3-beta.4+build.5",
        "2.3.4-beta.1",
        "4.5.6",
    ]:
        print()
        print(f'--- ({nbver})')

        version_data = parser(nbver)

        print(version_data)
        print(repr(version_data))

        print(f"major             = {version_data.major}")
        print(f"minor             = {version_data.minor}")
        print(f"patch             = {version_data.patch}")
        print(f"prerelease        = {version_data.prerelease}")
        print(f"build             = {version_data.build}")

        print(f"next (prerelease) = {version_data.next_version(part="prerelease")}")

    print()

# Corrupted data.
    nbver = "2.3"

    print(f'--- ({nbver}) --> CORRUPTED!')

    version_data = parser(nbver)
