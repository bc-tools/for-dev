#### 'TESTS' section (mandatory)








XXX



~~~python
# Extract of UnixName class code (2026-11-01).

# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    import pytest

    from aboutmeta.core.errors import YAMLTypeError

# debug:
    yaml_data = 'de-bug_ing'
    mydata    = UnixName(name = yaml_data)

    print('---')
    print(f"{yaml_data = }")
    print(f"{mydata    = }")
# :debug

# test: legal unix names
    yaml_data = '_abc-cde123'
    mydata    = UnixName(name = yaml_data)

    assert mydata.name == yaml_data

# test: illegal yaml data type
    for yaml_data in [
        None,
        123,
    ]:
        with pytest.raises(YAMLTypeError) as e:
            UnixName(name = yaml_data)

# debug:
        print('---')
        print(e)
# :debug
~~~

code automatiquement fabriqué, utile pour comprendre usage de

~~~python
# Extract of UnixName class unit tests (2026-11-01).

import pytest

from aboutmeta.core.errors import YAMLTypeError

def test_legal_unix_names():
    yaml_data = '_abc-cde123'
    mydata    = UnixName(name = yaml_data)

    assert mydata.name == yaml_data

@pytest.mark.parametrize(
    "yaml_data",
    [None, 123]
)
def test_illegal_yaml_data_type(yaml_data):
    with pytest.raises(YAMLTypeError) as e:
        UnixName(name = yaml_data)

...
~~~


You must provide a minimum set of use cases to serve as the foundation for testing the accepted contributions. **Be sure to include both functional examples and edge cases with corrupted data!**


If tests are not applicable, please use the following snippet to explicitly state that no tests are required.
Note that the line `# No test!` must be right after `if __name__ == "__main__":`.

~~~python
# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# No test!
    ...
~~~


> ***WARNING.*** *If the 'TESTS' section is missing, the continuous integration process will fail, as tests are assumed to be missing.*
