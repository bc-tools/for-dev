#!/usr/bin/env python3

from aboutmeta.core.errors import ParsingError


# -------------------------------------- #
# -- DATA FRAMED AT THE END OF A TEXT -- #
# -------------------------------------- #

###
# prototype::
#     content       : text with, or without, a specific extremal
#                     data surrounded by the delimiters defined
#                     using the ''delims'' argument.
#     delims        : list of opening and closing string delimiters
#                     used to enclose special data.
#     context       : context of use (this text is for error
#                     messages).
#     data_on_right : if the value is ''True'', the 'enclosed' data
#                     must be at the end of the text, otherwise it
#                     must be at the beginning (no data can be
#                     inside the text).
#
#     :return: pair of variables ''(remaining, data)'' where
#              ''remaining'' is the text obtained after removing
#              the 'enclosed' data. ''data'' is ''None'' if no data
#              has been extracted, and all constructed texts are
#              stripped.
#
#
# tip::
#     For single characters, you can directly pass a 2-length string.
#
#
# Here is a terminal session without any error.
#
# pyterm::
#     > from aboutmeta.tools.group import extract_group
#     > extract_group('Nothing to extract', '{}', 'OK.1')
#     ('Nothing to extract', None)
#     > extract_group('We have {  data }', '{}', 'OK.2')
#     ('We have', 'data')
#     > extract_group('{Data} before', '{}', 'OK.3', False)
#     ('before', 'Data')
#     > extract_group('We have {{data[--', ['{{', '[--'], 'OK.3')
#     ('We have', 'data')
#
#
# Here is a terminal session with errors.
#
# pyterm::
#     > from aboutmeta.tools.group import extract_group
#     > extract_group('Not opened!}', '{}', 'KO1')
#     Traceback (most recent call last):
#       ...
#         raise ParsingError(
#     aboutmeta.core.errors.ParsingError: missing opening ''{'' for KO1.
#     > extract_group('Not {closed!', '{}', 'KO2')
#     Traceback (most recent call last):
#       ...
#         raise ParsingError(
#     aboutmeta.core.errors.ParsingError: missing closing ''}'' for KO2.
#     > extract_group('Mis}placed{ delims', '{}', 'KO3')
#     Traceback (most recent call last):
#       ...
#         raise ParsingError(
#     aboutmeta.core.errors.ParsingError: missing closing ''}'' at the end for KO3.
#     > extract_group('{Bad data} before', '{}', 'KO4')
#     Traceback (most recent call last):
#       ...
#         raise ParsingError(
#    aboutmeta.core.errors.ParsingError: missing closing ''}'' at the end for KO4.
###
def extract_group(
    content      : str,
    delims       : str | list[str],
    context      : str,
    data_on_right: bool = True
) -> tuple[str, str | None]:
# Two delimiters?
    if len(delims) != 2:
        raise ValueError(
            f"two delimiters needed, see '{delims}'."
        )

    opener, closer = delims

# No delimiter used.
    if (
        not closer in content
        and
        not opener in content
    ):
        return (content, None)

# One of the delimiters is alone. Poor lonesome delimiter...
    for missing, found, kind in [
        (closer, opener, 'closing'),
        (opener, closer, 'opening'),
    ]:
        if (
            not missing in content
            and
            found in content
        ):
            raise ParsingError(
                f'missing {kind} {missing!r} for {context}.'
            )

# Good use of delimiters?
    if data_on_right:
        extrem_start = len(content) - len(closer)
        extrem_end   = len(content)
        extrem_char  = closer

    else:
        extrem_start = 0
        extrem_end   = len(opener)
        extrem_char  = opener

    if content[extrem_start: extrem_end] != extrem_char:
        if extrem_start == 0:
            what  = 'opening'
            where = 'begining'

        else:
            what  = 'closing'
            where = 'end'

        raise ParsingError(
            f'at {where}, missing {what} {extrem_char!r} '
            f'for {context}.'
        )

# Let's extract special data.
    if extrem_start == 0:
        end       = content.index(closer)
        data      = content[extrem_end: end].strip()
        remaining = content[end + len(closer):].strip()

    else:
        start     = content.rindex(opener)
        data      = content[start + len(opener): extrem_start].strip()
        remaining = content[:start].strip()

# Mission accomplished.
    return (remaining, data)


###
# prototype::
#     groups : list of texts to be enclosed.
#     delims : texts indicating 'framing' characters.
#            @ len(groups) = len(delims)
#
#     :return: text obtained by joining the enclosed texts with
#              spaces.
#
#
# Here is a terminal session.
#
# pyterm::
#     > from aboutmeta.tools.group import gather_groups
#     > gather_groups(
#         ['Someone', 'email@test.org', 'Institute, Galaxy'],
#         ['', '[]', '()']
#     )
#     'Someone [email@test.org] (Institute, Galaxy)'
#     > gather_groups(
#         ['Someone', '', 'Institute, Galaxy'],
#         ['', '[]', '()']
#     )
#     'Someone (Institute, Galaxy)'
#     > gather_groups(
#         ['Someone', 'email@test.org', 'Institute, Galaxy'],
#         ['', '[', '()']
#     )
#     Traceback (most recent call last):
#     ...
#         raise ValueError(
#     ValueError: two characters needed as delimiters, see '[' in delims = ['', '[', '()'].
#     > gather_groups(
#         ['Someone', 'email@test.org', 'Institute, Galaxy'],
#         ['[]', '()']
#     )
#     Traceback (most recent call last):
#     ...
#         raise ValueError('groups and delims must have the same length.')
#     ValueError: lists ''groups'' and ''delims'' must have the same length.
###
def gather_groups(
    groups: list[str],
    delims: list[str],
) -> str:
# Same sizes?
    if len(groups) != len(delims):
        raise ValueError(
            "lists 'groups' and 'delims' must have same length."
        )

# Let's apply the delimiters.
    content = []

    for grp, dlm in zip(groups, delims):
# We need two delimiters, or zero.
        if (
            dlm != ''
            and
            len(dlm) != 2
        ):
            raise ValueError(
                 'two characters delimiters needed, '
                f'see {dlm!r} in delims = {delims!r}.'
            )

# A new group.
        if grp:
            if dlm:
                l, r = dlm
                grp  = f'{l}{grp}{r}'

            content.append(grp)

# Eveything looks good.
    content = ' '.join(content)

    return content


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == '__main__':
# dev:
    INTERACTIVE_SESSION = True
    INTERACTIVE_SESSION = False
# :dev

    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

# dev:
    if INTERACTIVE_SESSION:
        print('---')

        content       = 'We have {{data[--'
        delims        = ['{{', '[--']
        data_on_right = True

        content       = '{{Data[-- before'
        delims        = ['{{', '[--']
        data_on_right = False

        print(f'{content      = }')
        print(f'{delims       = }')
        print(f'{data_on_right = }')

        print()
        print(
            f'extract_group: {extract_group(content, delims, "DEBUGGING", data_on_right)}'
        )

        exit()
# :dev

# -- Extract groups - Legal spec (data on left) -- #
    @given(
        full_data = st.sampled_from([
            (
                'We have no data',
                ('We have no data', None),
                '[]',
            ),
            (
                'We [h]ave [data]',
                ('We [h]ave', 'data'),
                '[]',
            ),
            (
                'We have ]data[',
                ('We have', 'data'),
                '][',
            ),
            (
                'We have {{data[--',
                ('We have', 'data'),
                ['{{', '[--'],
            ),
        ]),
    )
    def test_legal_spec_data_on_right(full_data) -> None:
        content, wanted_tuple, delims = full_data

        assert extract_group(
            content = content,
            delims  = delims,
            context = "LEGAL SPEC DATA ON LEFT",
        ) == wanted_tuple

    test_legal_spec_data_on_right()

# -- Extract groups - Legal spec (data on right) -- #
    @given(
        full_data = st.sampled_from([
            (
                'We have no data',
                ('We have no data', None),
                '()',
            ),
            (
                '(Data) we (h)ave',
                ('we (h)ave', 'Data'),
                '()',
            ),
            (
                ')Data( we have',
                ('we have', 'Data'),
                ')(',
            ),
            (
                '---]Data}}} we have',
                ('we have', 'Data'),
                ['---]', '}}}'],
            ),
        ]),
    )
    def test_legal_spec_data_on_right(full_data) -> None:
        content, wanted_tuple, delims = full_data

        assert extract_group(
            content      = content,
            delims       = delims,
            context      = "LEGAL SPEC DATA ON RIGHT",
            data_on_right = False
        ) == wanted_tuple

    test_legal_spec_data_on_right()









    exit()

    for i, (txt, delims) in enumerate(
        [
            (
                'Not [closed!',
                '[]',
            ),
            (
                'Mis]placed[ delims',
                '[]',
            ),
            (
                '[Bad data] before',
                '[]',
            ),
        ],
        start = 1
    ):
        ctxt = f'-- CTXT KO {i} --'

        print()
        print(ctxt)

        print(f'{txt    = }')
        print(f'{delims = }')

        try:
            extract_group(txt, delims, ctxt)

        except ParsingError as e:
            print(f'ParsingError: {e}')

    exit()

    print('\n------------\n')

    print('## gather_groups ##')

    for i, (txtgps, delims) in enumerate(
        [
            (
                ['Someone', 'email@test.org', 'Institute, Galaxy'],
                ['', '[]', '()']
            ),
            (
                ['Someone', '', 'Institute, Galaxy'],
                ['', '[]', '()']
            ),
        ],
        start = 1
    ):
        print()
        print(f'-- CTXT OK {i} --')

        print(f'{txtgps = }')
        print(f'{delims = }')
        print(
                'result =',
            gather_groups(txtgps, delims)
        )

    for i, (txt, delims) in enumerate(
        [
            (
                ['Someone', 'email@test.org', 'Institute, Galaxy'],
                ['', '[', '()']
            ),
            (
                ['Someone', 'email@test.org', 'Institute, Galaxy'],
                ['[]', '()']
            ),
        ],
        start = 1
    ):
        print()
        print(f'-- CTXT KO {i} --')

        try:
            print(f'{txtgps = }')
            print(f'{delims = }')

            gather_groups(txtgps, delims)

        except ValueError as e:
            print(f'ValueError: {e}')
