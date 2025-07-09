#!/usr/bin/env python3

import aboutmeta


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

        v = parser(nbver)

        print(v)
        print(repr(v))

        print(f"major      = {v.major}")
        print(f"minor      = {v.minor}")
        print(f"patch      = {v.patch}")
        print(f"prerelease = {v.prerelease}")
        print(f"build      = {v.build}")

    print()

# Corrupted data.
    nbver = "2.3"

    print(f'--- ({nbver}) --> CORRUPTED!')

    v = parser(nbver)
