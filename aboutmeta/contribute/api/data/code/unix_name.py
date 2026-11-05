#!/usr/bin/env python3

# TODO  REVOIR ! L'iédée est d'avoir un nommage standard : https://www.cyberciti.biz/faq/linuxunix-rules-for-naming-file-and-directory-names/

import re


from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError
from aboutmeta.core.validate     import validate_type


# ---------- #
# -- DATA -- #
# ---------- #

PATTERN_UNIX_NAME = re.compile(r'^[a-z_][a-z0-9_-]*$')


###
# prototype:
#     name : a \unix-style name that only uses lowercase letters,
#            digits, underscores, and hyphens, and cannot start
#            with a digit or a hyphen.
###
class UnixName(DataManager):
    name: str

###
# prototype:
#     :action: mandatory validations of ''self.URL'' type, and
#              the \unix name format.
###
    def __post_init__(self) -> None:
        validate_type(
            data_name      = 'Unix name',
            data           = self.name,
            types_expected = str,
        )

        if not PATTERN_UNIX_NAME.match(self.name):
            raise ParsingError(
                f'Unvalid Unix name "{self.name}".'
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

    from aboutmeta.core.errors import YAMLTypeError

# dev:
    yaml_data = 'de-bug_ing'
    mydata    = UnixName(name = yaml_data)

    print('---')
    print(f"{yaml_data = }")
    print(f"{mydata    = }")
# :dev


# -- Legal UNIX names -- #
    def test_legal_name(yaml_data):
        yaml_data = '_abc-cde123'
        mydata    = UnixName(name = yaml_data)

        assert mydata.name == yaml_data

    test_legal_name()


# -- Illegal YAML data type -- #
    @given(
        yaml_data = st.sampled_from([
            None,
            123,
        ]),
    )
    def test_illegal_data_type(yaml_data):
        with pytest.raises(YAMLTypeError) as e:
            UnixName(name = yaml_data)

# dev:
        print('---')
        print(e)
# :dev

    test_illegal_data_type()


# -- Illegal UNIX names -- #
    @given(
        yaml_data = st.sampled_from([
            '-hyphen-pb',
            'CasePB',
            '123-digits-pb',
        ]),
    )
    def test_illegal_name(yaml_data):
        with pytest.raises(ParsingError) as e:
            UnixName(name = yaml_data)

# dev:
        print('---')
        print(e)
# :dev

    test_illegal_name()
