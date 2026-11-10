#!/usr/bin/env python3


# ------------- #
# -- PARSING -- #
# ------------- #

###
# prototype::
#     data_name      : XXXXX
#     data           : XXXXX
#     expected_types : XXXXX
#
#     :action: XXXXX
###
def validate_type(
    data_name     : str,
    data          : object,
    expected_types: object,
) -> None:
    if not isinstance(data, expected_types):
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
            f'{data_name} data: value = {data!r}.'
        )


# --------------------- #
# -- NOTHING TO TEST -- #
# --------------------- #
