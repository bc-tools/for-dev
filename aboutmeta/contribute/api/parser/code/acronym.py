#!/usr/bin/env python3

###
# The origin of an acronym can be explained using a tiny \dsl.
# For example, ''[A::@-]bout [Desc]ription'' explains the
# choice of the acronym "@-Desc" for "About Description".
# Here is how it works.
#
#     1) First, we have the full name ''About Description''.
#
#     1) Then, we indicate inside brackets the parts to keep
#     for the acronym. Using ''[A]bout [Desc]ription'' will
#     produce the acronym "Adesc".
#
#     1) Finally, ''::'' in ''[A::@-]'' indicates the use of
#     "@-" instead of "A" in the acronym.
###


from aboutmeta.specs.data.acronym import Acronym


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : acronym \spec provided in the \yaml file.
#
#     :return: ''Acronym'' instance representing the acronym.
###
def parse(data: str) -> Acronym:
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.acronym.Acronym''.
    return Acronym(spec = data)


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : ''Acronym'' object.
#
#     :return: std \yaml version of the ''Acronym'' object.
###
def write(data: Acronym) -> str:
    return data.spec


# ----------- #
# -- TESTS -- #
# ----------- #

# We just need some basic interface tests, because we have
# already tested the ''Acronym'' class.

if __name__ == "__main__":
    from hypothesis import (
        given,
        strategies as st
    )

# dev:
    yaml_data   = "[about::@] [meta]data"
    data_parsed = parse(yaml_data)

    print('---')
    print(f"{yaml_data          = }")
    print(f"{data_parsed        = }")
    print(f"{write(data_parsed) = }")
# :dev

# -- Back to spec -- #
    @given(
        yaml_data = st.sampled_from([
            "[about::@] [meta]data",
        ]),
    )
    def test_back_2_spec(yaml_data: str) -> None:
        assert write(parse(yaml_data)) == yaml_data

    test_back_2_spec()
