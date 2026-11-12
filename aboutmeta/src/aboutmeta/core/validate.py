#!/usr/bin/env python3


# ------------- #
# -- PARSING -- #
# ------------- #

###
# prototype::
#     var_name       : variable name (for error message).
#     value          : variable value.
#     expected_types : the types allowed for ''value''.
#
#     :action: validate the ''value'' type.
###
def validate_type(
    var_name      : str,
    value         : object,
    expected_types: object,
) -> None:
    if not isinstance(value, expected_types):
        if isinstance(expected_types, tuple):
            types_desc = ', '.join(
                sorted(
                    f'{t.__name__!r}'
                    for t in expected_types
                )
            )

            types_desc = f'[{types_desc}]'

        else:
            types_desc = f'{expected_types.__name__!r}'

        raise TypeError(
            f'None {types_desc} '
            f'{var_name} value: value = {value!r}.'
        )


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

# -- Legal type -- #
    @given(
        full_data = st.sampled_from([
            (2  , int),
            ('2', str),
            (2  , (float, int)),
        ]),
    )
    def test_legal_type(full_data) -> None:
        val, _type = full_data

        validate_type(
            var_name       = '',
            value          = val,
            expected_types = _type,
        )

    test_legal_type()

# -- Illegal type -- #
    @given(
        full_data = st.sampled_from([
            (2, str),
            (2, float),
        ]),
    )
    def test_illegal_type(full_data) -> None:
        val, _type = full_data

        with pytest.raises(TypeError) as e:
            validate_type(
                var_name       = '',
                value          = val,
                expected_types = _type,
            )

    test_illegal_type()
