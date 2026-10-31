#!/usr/bin/env python3

import re


from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError
from aboutmeta.core.validate     import validate_type


# ---------- #
# -- DATA -- #
# ---------- #

PATTERN_UNIX_NAME = re.compile(r'^[a-z_][a-z0-9_-]*$')


###
# prototype::
#     name : a \unix-style name that only uses lowercase letters,
#            digits, underscores, and hyphens, and cannot start
#            with a digit or a hyphen.
###
class UnixName(DataManager):
    name: str

###
# prototype::
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
    import pytest

    from aboutmeta.core.errors import YAMLTypeError

# DEBUG ON
    yaml_data = 'de-bug_ing'
    mydata    = UnixName(name = yaml_data)

    print('---')
    print(f"{yaml_data = }")
    print(f"{mydata    = }")
# DEBUG OFF

# test: legal unix names
    for yaml_data in [
        '_abc-cde123',
    ]:
        mydata = UnixName(name = yaml_data)

        assert mydata.name == yaml_data

# test: illegal yaml data type
    for yaml_data in [
        None,
        123,
    ]:
        with pytest.raises(YAMLTypeError) as e:
            UnixName(name = yaml_data)

# DEBUG ON
        print('---')
        print(e)
# DEBUG OFF

# test: illegal unix names
    for yaml_data in [
        '-hyphen-pb',
        'CasePB',
        '123-digits-pb',
    ]:
        with pytest.raises(ParsingError) as e:
            UnixName(name = yaml_data)

# DEBUG ON
        print('---')
        print(e)
# DEBUG OFF
