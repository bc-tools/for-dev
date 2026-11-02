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

PATTERN_ACRONYM_METADATA = re.compile(
    r'\[\s*(.*?)(?:\s*::\s*(.*?))?\s*\]|([^\[]+)'
)

TAG_ACRONYM_DEF_OPEN, TAG_ACRONYM_DEF_CLOSE = '[]'


###
# prototype::
#     spec  : the \spec of an acronym using brackets.
#     short : the acronym alone.
#     desc  : the \def of acronym without any bracket.
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
            types_expected = str,
        )

# We only keep internal extra spaces.
        self.spec = self.spec.strip()

# Good use of the square brackets?
        bracket_is_opened = False

        for i, c in enumerate(self.spec):
            if c == TAG_ACRONYM_DEF_OPEN:
                if bracket_is_opened:
                    raise ParsingError('Unclosed bracket group.')

                else:
                    bracket_is_opened = True

            elif c == TAG_ACRONYM_DEF_CLOSE:
                if not bracket_is_opened:
                    raise ParsingError('Unopened bracket group.')

                else:
                    bracket_is_opened = False

        if bracket_is_opened:
            raise ParsingError('Unclosed bracket group.')

# Extract the spec parts.
        spec_parts = []

        for match in PATTERN_ACRONYM_METADATA.finditer(self.spec):
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

if __name__ == "__main__":
    import pytest

    from aboutmeta.core.errors import YAMLTypeError

    import random

# debug:
    yaml_data = '[about] [meta]data'
    mydata    = Acronym(spec = yaml_data)

    print('---')
    print(f"{yaml_data = }")
    print(f"{mydata    = }")
# :debug

# test: legal specs
    for yaml_data, short, desc in [
        (
            "[about] [meta]data",
            "aboutmeta",
            "about metadata",
        ),
        (
            "[about::@-] [meta::met-@]data",
            "@-met-@",
            "about metadata",
        ),
    ]:
        mydata = Acronym(spec = yaml_data)

        assert mydata.spec == yaml_data
        assert mydata.short == short
        assert mydata.desc == desc



    exit()

# test: weird legal spacing
    for yaml_data in [
        "[about] [meta]data",
        "[about::@-] [meta::met-@]data",
    ]:


        weird_spec = yaml_data



        mydata = Acronym(spec = yaml_data)

        assert mydata.spec == std_spec










# test: illegal yaml data type
    for yaml_data in [
        None,
        123,
    ]:
        with pytest.raises(YAMLTypeError) as e:
            Acronym(spec = yaml_data)

# debug:
        print('---')
        print(f"{yaml_data = }")
        print(e)
# :debug


# test: illegal specs
    for yaml_data in [
        "about metadata",
        "[about [meta]data",
        "[about] meta]data",
        "[about metadata",
        "about meta]data",
    ]:
        with pytest.raises(ParsingError) as e:
            Acronym(spec = yaml_data)

# debug:
        print('---')
        print(f"{yaml_data = }")
        print(e)
# :debug
