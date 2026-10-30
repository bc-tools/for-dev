#!/usr/bin/env python3

###
# Semantic version \nbs must comply with cf::''Semantic
# Versioning ; https://semver.org/'' like nbver::''1.0.0'',
# nbver::''0.0.0-beta.1'', and nbver::''0.3.1-beta.1+build.5''.
###


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
#     :return: an instance of the ''semver.Version'' class
#              representing the \nbver.
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
#     :return: the \std \yaml version of the ''semver.Version''
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

    for std_yaml_data in [
        "1.2.3-beta.4+build.5",
        "2.3.4-beta.1",
        "4.5.6",
    ]:
        data_parsed = parse(std_yaml_data)

        print()
        print('~~~')

        print()
        print(f"{std_yaml_data      = }")
        print(f"{data_parsed        = }")
        print(f"{write(data_parsed) = }")

        print()
        print( f"repr(data_parsed)      = {data_parsed!r}")
        print(f"{data_parsed.major      = }")
        print(f"{data_parsed.minor      = }")
        print(f"{data_parsed.patch      = }")
        print(f"{data_parsed.prerelease = }")
        print(f"{data_parsed.build      = }")

        print()
        print(f"{data_parsed.next_version(part="prerelease") = }")

    print()


# BAD
    # exit()

    print("\n------------\n")

    print("-- BAD CASES --")

    for std_yaml_data in [
        "2.3",
    ]:
        print()

        print(f'{std_yaml_data = }')

        try:
            parse(std_yaml_data)

        except Exception as e:
            print(type(e).__name__, ':', e)

            notes = getattr(e, "__notes__", [])

            for i, n in enumerate(notes, start = 1):
                print(f'[{i}]. {n}')
