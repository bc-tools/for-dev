#!/usr/bin/env python3


# ------------- #
# -- PARSING -- #
# ------------- #

###
# prototype::
#     var_name       : name of the variable
#     value          : XXXXX
#     expected_types : XXXXX
#
#     :action: XXXXX
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


# --------------------- #
# -- NOTHING TO TEST -- #
# --------------------- #
