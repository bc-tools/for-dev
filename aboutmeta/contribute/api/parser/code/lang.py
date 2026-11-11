#!/usr/bin/env python3

###
# A \lang is indicated using an cf::''ISO 639 standard ;
# https://en.wikipedia.org/wiki/ISO_639'' short identifier, then,
# if necessary, adding a country using a cf::''ISO 3166
# standard ; https://en.wikipedia.org/wiki/ISO_3166'' classifier.
# For example, ''fr'' indicates "France French", whereas ''fr-BE''
# indicates "Belgian French".
#
#
# tip::
#     You can use ''_'' instead of ''-''. This is useful when
#     pasting external text or more efficient when typing.
###


from aboutmeta.specs.data.lang import Lang


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : \lang provided in the \yaml file.
#
#     :return: ''Lang'' instance representing the \lang.
###
def parse(data: str) -> Lang:
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.lang.Lang''.
    return Lang(std_id = data)


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : ''Lang'' object.
#
#     :return: full \lang identifier like ''"fr-FR"''.
###
def write(data: Lang) -> str:
    return data.std_id


# ----------- #
# -- TESTS -- #
# ----------- #

# We just need some basic interface tests, because we have already
# tested the ''Lang'' class.

if __name__ == "__main__":
    from hypothesis import (
        given,
        strategies as st
    )

# dev:
    yaml_data   = "fr"
    data_parsed = parse(yaml_data)

    print('---')
    print(f"{yaml_data          = }")
    print(f"{data_parsed        = }")
    print(f"{write(data_parsed) = }")
# :dev

# -- Back to spec -- #
    @given(
        yaml_data = st.sampled_from([
            "fr-BE",
        ]),
    )
    def test_back_2_spec(yaml_data: str) -> None:
        assert write(parse(yaml_data)) == yaml_data

    test_back_2_spec()
