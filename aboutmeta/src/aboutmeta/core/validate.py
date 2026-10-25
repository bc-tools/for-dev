#!/usr/bin/env python3


# ------------- #
# -- PARSING -- #
# ------------- #

###
# Parsing errors must use the ''ParsingError'' class.
###
def validate_type(
    data_name    : str,
    data         : object,
    type_expected: object,
) -> None:
    if not isinstance(data, type_expected):
        if isinstance(type_expected, tuple):
            types_desc = ', '.join(
                sorted(
                    f'{t.__name__!r}'
                    for t in type_expected
                )
            )

            types_desc = f'[{types_desc}]'

        else:
            types_desc = f'{types_desc.__name__!r}'

        raise ValueError(
            f'None {types_desc} '
            f'{data_name}: value = {data!r}.'
        )


# --------------------- #
# -- NOTHING TO TEST -- #
# --------------------- #
