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
#     data : the \str_data provided in the \yaml file, but stripped.
#
#     :return: an instance of the ''semver.Version'' class.
###
def parse(data: str) -> Version:
    try:
        version = VersionInfo.parse(data)

    except ValueError as e:
        raise ParsingError(e)

    return version


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''semver.Version'' object.
#
#     :return: the standard \yaml version of the ''semver.Version''
#              object.
###
def write(data: Version) -> str:
    return str(data)


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print()
    print("-- GOOD CASES --")

    for str_data in [
        "1.2.3-beta.4+build.5",
        "2.3.4-beta.1",
        "4.5.6",
    ]:
        data_parsed = parse(str_data)

        print()
        print('~~~')

        print()
        print(f"{str_data = }")

        print()
        print( f"repr(data_parsed)      = {data_parsed!r}")
        print(f"{data_parsed.major      = }")
        print(f"{data_parsed.minor      = }")
        print(f"{data_parsed.patch      = }")
        print(f"{data_parsed.prerelease = }")
        print(f"{data_parsed.build      = }")

        std_yaml_data = write(data_parsed)

        print()
        print(f"{std_yaml_data = }")

        print()
        print(f"{data_parsed.next_version(part="prerelease") = }")

    print()


# BAD
    # exit()

    print("\n------------\n")

    print("-- BAD CASES --")

    for str_data in [
        "2.3",
    ]:
        print()

        print(f'{str_data = }')

        try:
            parse(str_data)

        except Exception as e:
            print(type(e).__name__, ':', e)

            notes = getattr(e, "__notes__", [])

            for i, n in enumerate(notes, start = 1):
                print(f'[{i}]. {n}')
