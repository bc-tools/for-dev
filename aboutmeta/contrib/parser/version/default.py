#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

from semver import (
    Version,
    VersionInfo,
)


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : the \nbver provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''semver.Version'' to work
#              easily with the number version.
###
def parser(content: str) -> Version:
    version = VersionInfo.parse(content)

    return version


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
# Working examples.
    for nbver in [
        "2.3.4-beta.1+build.5",
        "2.3.4-beta.1",
        "2.3.4",
    ]:
        print()
        print(f'--- ({nbver})')

        version_data = parser(nbver)

        print(version_data)
        print(repr(version_data))

        print(f"major      = {version_data.major}")
        print(f"minor      = {version_data.minor}")
        print(f"patch      = {version_data.patch}")
        print(f"prerelease = {version_data.prerelease}")
        print(f"build      = {version_data.build}")

    print()

# Corrupted data.
    nbver = "2.3"

    print(f'--- ({nbver}) --> CORRUPTED!')

    version_data = parser(nbver)
