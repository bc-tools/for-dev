#!/usr/bin/env python3

from semver import (
    Version,
    VersionInfo,
)

from aboutmeta.core.errors import ParsingError


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : the \nbver provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''semver.Version'' to work
#              easily with the number version.
###
def parse(data: str) -> Version:
    try:
        version = VersionInfo.parse(data)

    except ValueError as e:
        raise ParsingError(e)

    return version


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    for nbver in [
        "1.2.3-beta.4+build.5",
        "2.3.4-beta.1",
        "4.5.6",
    ]:
        print()

        version_data = parse(nbver)

        print(f"{nbver                                        = }")
        print( f"repr(version_data)                           = {version_data!r}")
        print(f"{version_data.major                           = }")
        print(f"{version_data.minor                           = }")
        print(f"{version_data.patch                           = }")
        print(f"{version_data.prerelease                      = }")
        print(f"{version_data.build                           = }")
        print(f"{version_data.next_version(part="prerelease") = }")

    print()


# BAD
    # exit()

    print("\n------------\n")

    print("-- BAD CASES --")

    for nbver in [
        "2.3",
    ]:
        print()

        print(f'{nbver = }')

        try:
            parse(nbver)

        except Exception as e:
            print(type(e).__name__, ':', e)

            notes = getattr(e, "__notes__", [])

            for i, n in enumerate(notes, start = 1):
                print(f'[{i}]. {n}')
