#!/usr/bin/env python3


# -------------------------- #
# -- TRANSFORMING STRINGS -- #
# -------------------------- #

###
# prototype::
#     text: text
#
#     part: part of the text we don't want surrounded by spaces.
#
#     :return: text stripped after cleaning up the spaces around
#         the ''part'' text.
#
#
# Here is a terminal session.
#
# pyterm::
#     > from aboutmeta.tools.spacing import no_space_around
#     > no_space_around('A -B  -  C  D-   G', '-')
#     'A-B-C  D-G'
#     > no_space_around(' -  ABC   - ', '-')
#     '-ABC-'
#     > no_space_around('  A   B    C  ', ' ')
#     'A B C'
#     > no_space_around('', ' ')
#     ''
###
def no_space_around(
    text: str,
    part: str
) -> str:
    text = [
        p.strip()
        for p in text.split(part)
        if p
    ]

    text = part.join(text)

    return text


###
# prototype::
#     text: text
#
#     :return: text stripped with multiple consecutive spaces
#         replaced by single spaces.
#
#     :see: no_space_around
#
#
# Here is a terminal session.
#
# pyterm::
#     > from aboutmeta.tools.spacing import single_spaces
#     > single_spaces('A   B    C')
#     'A B C'
#     > single_spaces('   A   B    C   ')
#     'A B C'
#     > single_spaces('')
#     ''
###
def single_spaces(text: str) -> str:
    return no_space_around(text, ' ')


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == '__main__':
# dev:
    INTERACTIVE_SESSION = True
    INTERACTIVE_SESSION = False
# :dev

    from random import Random

    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

    from string import (
        ascii_letters,
        punctuation
    )

# dev:
    if INTERACTIVE_SESSION:
        print('---')

        txt  = 'aMFky        !       AA   !  AA   !                  '
        part = '!'

        print(f'{txt                        = }')
        print(f'{part                       = }')
        print(f'{no_space_around(txt, part) = }')

        print('---')

        txt = 'AA AA AA'

        print(f'{txt                = }')
        print(f'{single_spaces(txt) = }')

        exit()
# :dev

# -- Tools for tests -- #
    def rnd_spacing(
        sentence: str,
        part    : str,
        rnd     : Random,
    ):
        _rnd_sentence = [' '*rnd.randint(0, 10)]

        words    = list(sentence.split(' '))
        nb_words = len(words)

        for i, w in enumerate(words, start = 1):
            _rnd_sentence += [
                w,
                ' '*rnd.randint(0, 10),
            ]

            if i != nb_words:
                _rnd_sentence += [
                    part,
                    ' '*rnd.randint(0, 10),
                ]

        _rnd_sentence.append(' '*rnd.randint(0, 10))

        rnd_sentence = ''.join(_rnd_sentence)

        return rnd_sentence

# -- No space around - Legal spec -- #
    @given(
        sentence = st.lists(
            st.text(
                alphabet = ascii_letters,
                min_size = 2,
                max_size = 10
            ),
            min_size = 3,
            max_size = 15
        ).map(" ".join),
        rnd = st.randoms(),
    )
    def test_no_space_around_legal_spec(
        sentence: str,
        rnd     : Random
    ) -> None:
        part = rnd.choice(punctuation)

        rnd_sentence = rnd_spacing(
            sentence = sentence,
            part     = part,
            rnd      = rnd,
        )

        sentence = sentence.replace(' ', part)

        assert no_space_around(
            text = rnd_sentence,
            part = part,
        ) == sentence

    test_no_space_around_legal_spec()

# -- Single spaces - Legal spec -- #
    @given(
        sentence = st.lists(
            st.text(
                alphabet = ascii_letters,
                min_size = 2,
                max_size = 10
            ),
            min_size = 3,
            max_size = 15
        ).map(" ".join),
        rnd = st.randoms(),
    )
    def test_single_spaces_legal_spec(
        sentence: str,
        rnd     : Random
    ) -> None:
        part        = rnd.choice(punctuation)
        rnd_sentence = rnd_spacing(
            sentence = sentence,
            part     = ' ',
            rnd      = rnd,
        )

        assert single_spaces(rnd_sentence) == sentence

    test_single_spaces_legal_spec()

# dev:
    print('LOCAL TESTS DONE..')
# :dev
