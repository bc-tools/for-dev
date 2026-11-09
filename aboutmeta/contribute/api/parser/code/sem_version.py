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
    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

# dev:
    yaml_data   = "1.2.3-beta.4+build.5"
    data_parsed = parse(yaml_data)

    print('---')
    print(f"{yaml_data              = }")
    print(f"{data_parsed            = }")
    print(f"{data_parsed.major      = }")
    print(f"{data_parsed.minor      = }")
    print(f"{data_parsed.patch      = }")
    print(f"{data_parsed.prerelease = }")
    print(f"{data_parsed.build      = }")
    print(f"{write(data_parsed)     = }")
# :dev

# -- Data - Illegal spec -- #
    @given(
        yaml_data = st.sampled_from([
            "2.3",
            "2-3-2025",
        ]),
    )
    def test_illegal_spec(yaml_data: str) -> None:
        with pytest.raises(ParsingError) as e:
            parse(yaml_data)

# dev:
        print('---')
        print(f'{yaml_data = }')
        print(e)
# :dev

    test_illegal_spec()

# -- Data - Illegal data type -- #
    @given(
        yaml_data = st.sampled_from([
            None,
            123,
        ]),
    )
    def test_illegal_data_type(yaml_data: object) -> None:
        with pytest.raises(TypeError) as e:
            parse(yaml_data)

# dev:
        print('---')
        print(f'{yaml_data = }')
        print(e)
# :dev

    test_illegal_data_type()

# -- Parser - Back to spec -- #
    @given(
        yaml_data = st.sampled_from([
            "4.5.6",
            "2.3.4-beta.1",
            "1.2.3-beta.4+build.5",
        ]),
    )
    def test_back_2_spec(yaml_data: str) -> None:
        assert write(parse(yaml_data)) == yaml_data

    test_back_2_spec()
