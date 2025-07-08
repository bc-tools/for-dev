#!/usr/bin/env python3

import aboutmeta


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

from semver import (
    Version,
    VersionInfo,
)

### TODO
# prototype::
#     content : XXX
#
#     :return: XXX
###
def parser(content: str) -> Version:
    version = VersionInfo.parse(content)

    return version


# ----------------------------- #
# -- HUMAN TESTS (MANDATORY) -- #
# ----------------------------- #

if __name__ == "__main__":
    for nbver in [
        "2.3.4-beta.1+build.5",
        "2.3.4-beta.1",
        "2.3.4",
        # "2.3",   # Test of an exception.
    ]:
        v = parser(nbver)

        print()
        print(f'--- ({v})')

        print(repr(v))

        print(f"major      = {v.major}")
        print(f"minor      = {v.minor}")
        print(f"patch      = {v.patch}")
        print(f"prerelease = {v.prerelease}")
        print(f"build      = {v.build}")

    print()
