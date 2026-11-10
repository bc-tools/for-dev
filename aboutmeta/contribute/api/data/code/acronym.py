#!/usr/bin/env python3

import re

from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError
from aboutmeta.core.validate     import validate_type

from aboutmeta.tools.misc  import single_spaces


# ---------- #
# -- DATA -- #
# ---------- #

PATTERN_METADATA = re.compile(
    r'\[\s*(.*?)(?:\s*::\s*(.*?))?\s*\]|([^\[]+)'
)

TAG__DEF_OPEN, TAG__DEF_CLOSE = '[]'


###
# prototype::
#     spec  : \spec of an acronym using brackets.
#     short : acronym alone.
#     desc  : full \def of acronym without any bracket.
#
#
# note::
#     The ''short'' and ''desc'' \attrs are build from the \val
#     of the ''spec'' \attr.
###
class Acronym(DataManager):
    spec : str
    short: str = field(init = False)
    desc : str = field(init = False)

###
# prototype::
#     :action: mandatory validations of ''self.spec'' type, and
#              derivation of the ''short'' and ''desc'' \attrs
#              from ''self.spec''.
###
    def __post_init__(self) -> None:
        validate_type(
            data_name      = 'spec',
            data           = self.spec,
            expected_types = str,
        )

# We only keep internal extra spaces.
        self.spec = self.spec.strip()

# Good use of the square brackets?
        bracket_is_opened = False

        for i, c in enumerate(self.spec):
            if c == TAG__DEF_OPEN:
                if bracket_is_opened:
                    raise ParsingError('Unclosed bracket group.')

                else:
                    bracket_is_opened = True

            elif c == TAG__DEF_CLOSE:
                if not bracket_is_opened:
                    raise ParsingError('Unopened bracket group.')

                else:
                    bracket_is_opened = False

        if bracket_is_opened:
            raise ParsingError('Unclosed bracket group.')

# Extract the spec parts.
        spec_parts = []

        for match in PATTERN_METADATA.finditer(self.spec):
            spec_initial, spec_final, other = match.groups()

            if not spec_initial is None:
                spec_initial = spec_initial.strip()

                if spec_final is None:
                    spec_final = spec_initial

                else:
                    spec_final = spec_final.strip()

                spec_parts.append((spec_initial, spec_final))

            elif not other is None:
                spec_parts.append((other, None))

# Build the short version.
        self.short = ''.join([
            p[1]
            for p in spec_parts
            if not p[1] is None
        ])

        if not self.short:
            raise ParsingError('Missing bracket group.')

# Build the raw description.
        self.desc = ''.join([
            p[0]
            for p in spec_parts
        ])

# Build the standard spec definition.
        self.spec = ''

        for p in spec_parts:
            if p[1] is None:
                self.spec += p[0]

            else:
                if p[0] == p[1]:
                    spec = p[0]

                else:
                    spec = '::'.join(p)

                self.spec += f'[{spec}]'


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == '__main__':
    from hypothesis import (
        given,
        strategies as st
    )

    import             pytest
    from random import Random

# dev:
    yaml_data = '[about] [meta]data    '
    mydata    = Acronym(spec = yaml_data)

    print('---')
    print(f'{yaml_data = }')
    print(f'{mydata    = }')
# :dev

# -- Legal spec -- #
    @given(
        full_data = st.sampled_from([
            (
                '[about] [meta]data',
                'aboutmeta',
                'about metadata'
            ),
            (
                '[about::@-] [meta::met-@]data',
                '@-met-@',
                'about metadata'
            ),
        ]),
    )
    def test_legal_spec(
        full_data: tuple[str, str, str]
    ) -> None:
        yaml_data, short, desc = full_data

        mydata = Acronym(spec = yaml_data)

        assert mydata.spec == yaml_data
        assert mydata.short == short
        assert mydata.desc == desc

    test_legal_spec()

# -- Weird spacing -- #
    @given(
        std_spec = st.sampled_from([
            '[about] [meta]data',
            '[about::@-] [meta::met-@]data',
        ]),
        rnd = st.randoms(),
    )
    def test_weird_spacing(
        std_spec: str,
        rnd     : Random
    ) -> None:
        weird_spec = std_spec

        for old in [
            '[{space}',
            '{space}]',
            '{space}::',
            '::{space}',
        ]:
            new = old.format(space = ' ' * rnd.randint(1, 5))

            weird_spec = weird_spec.replace(
                old.replace('{space}', ''),
                new
            )

        weird_data = Acronym(spec = weird_spec)

        assert weird_data.spec == std_spec

    test_weird_spacing()

# -- Illegal spec -- #
    @given(
        yaml_data = st.sampled_from([
            'about metadata',
            '[about [meta]data',
            '[about] meta]data',
            '[about metadata',
            'about meta]data',
        ]),
    )
    def test_illegal_spec(yaml_data: str) -> None:
        with pytest.raises(ParsingError) as e:
            Acronym(spec = yaml_data)

# dev:
        print('---')
        print(f'{yaml_data = }')
        print(e)
# :dev

    test_illegal_spec()

# -- Illegal data type -- #
    @given(
        yaml_data = st.sampled_from([
            None,
            123,
        ]),
    )
    def test_illegal_data_type(yaml_data: object) -> None:
        with pytest.raises(TypeError) as e:
            Acronym(spec = yaml_data)

# dev:
        print('---')
        print(f'{yaml_data = }')
        print(e)
# :dev

    test_illegal_data_type()
