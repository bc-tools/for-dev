#!/usr/bin/env python3

from langcodes import (
    get as get_langcode,
    LanguageTagError
)


from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError
from aboutmeta.core.validate     import validate_type


# ---------- #
# -- DATA -- #
# ---------- #

###
# prototype:
#     std_id    : the \std \lang identifier like ''"en-GB"''.
#     name      : the full \lang name like ''"English"''.
#     territory : the territory of the \lang like ''"Great
#                 Britain"''.
#
#
# note:
#     The ''name'' and ''territory'' \attrs are build from the
#     \val of the ''std_id'' \attr.
#
#
# warning:
#     Short identifiers are automatically expanded to full ones
#     regardless of letter casing: ''"fr"'' and ''"FR-fr"'' are
#     saved as ''"fr-FR"''.
#     Enforcing this normalization \std at the \yaml input stage
#     is a painless best practice.
###
class Lang(DataManager):
    std_id   : str
    name     : str = field(init = False)
    territory: str = field(init = False)

###
# prototype:
#     :action: mandatory validations of ''self.std_id'' type, and
#              derivation of the ''name'' and ''territory'' \attrs
#              from ''self.std_id'' and expand the identifier to
#              its full form (e.g., ''"fr"'' becomes ''"fr-FR"'').
###
    def __post_init__(self) -> None:
        validate_type(
            data_name      = 'std_id',
            data           = self.std_id,
            types_expected = str,
        )

# Getting a normalized code.
        try:
            lang = get_langcode(self.std_id.strip()).maximize()

        except LanguageTagError as e:
            msg = str(e)
            msg = msg[0].lower() + msg[1:]

            raise ParsingError(msg)

# Small description of the language code.
        desc = lang.describe('en')

# Patch for the strange "Unknow language".
        if desc['language'].startswith('Unknown language'):
            raise ValueError(
                f"unknown language code '{self.std_id}'"
            )

# The job has been done.
        self.std_id    = f"{lang.language}-{lang.territory}"
        self.name      = desc["language"]
        self.territory = desc["territory"]


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

    from aboutmeta.core.errors import YAMLTypeError

# dev:
    yaml_data = 'it   '
    mydata    = Lang(std_id = yaml_data)

    print('---')
    print(f"{yaml_data = }")
    print(f"{mydata    = }")
# :dev

# -- Legal spec -- #
    @given(
        full_data = st.sampled_from([
            (
                'fr', 'fr-FR',
                'French', 'France',
            ),
            (
                'en', 'en-US',
                'English', 'United States',
            ),
            (
                'en-GB', 'en-GB',
                'English', 'United Kingdom',
            ),
        ]),
    )
    def test_legal_spec(full_data):
        yaml_data, std_id, name, territory = full_data

        mydata = Lang(std_id = yaml_data)

        assert mydata.std_id == std_id
        assert mydata.name == name
        assert mydata.territory == territory

    test_legal_spec()

# -- Legal weird letter casing -- #
    @given(
        std_id = st.sampled_from([
            "fr-BE",
            "es-ES",
            "en-US",
        ]),
        rnd = st.randoms(),
    )
    def test_weird_letter_casing(std_id, rnd):
        weird_id = ''.join([
            rnd.choice([c.lower(), c.upper()])
            for c in std_id
        ])

        for sep in '-_':
            weird_id = weird_id.replace('-', sep)

        weird_data = Lang(std_id = weird_id)

        assert weird_data.std_id == std_id

    test_weird_letter_casing()

# -- Unknown lang -- #
    @given(
        yaml_data = st.sampled_from([
            "XXX",
        ]),
    )
    def test_unknown_lang(yaml_data):
        with pytest.raises(ValueError) as e:
            Lang(std_id = yaml_data)

# dev:
        print('---')
        print(f"{yaml_data = }")
        print(e)
# :dev

    test_unknown_lang()

# -- Illegal lang ID -- #
    @given(
        yaml_data = st.sampled_from([
            "X.X",
        ]),
    )
    def test_illegal_lang_ID(yaml_data):
        with pytest.raises(ParsingError) as e:
            Lang(std_id = yaml_data)

# dev:
        print('---')
        print(f"{yaml_data = }")
        print(e)
# :dev

# -- Illegal YAML data type -- #
    @given(
        yaml_data = st.sampled_from([
            None,
            123,
        ]),
    )
    def test_illegal_yaml_data_type(yaml_data):
        with pytest.raises(YAMLTypeError) as e:
            Lang(std_id = yaml_data)

# dev:
        print('---')
        print(f"{yaml_data = }")
        print(e)
# :dev

    test_illegal_yaml_data_type()
