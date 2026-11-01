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
~~~

code automatiquement fabriqué, utile pour comprendre usage de

~~~python
# Extract of UnixName class unit test (2026-11-01).

@pytest.mark.parametrize(
    "yaml_data",
    [
        '-hyphen-pb',
        'CasePB',
        '123-digits-pb',
    ]
)
def test_illegal_unix_names(yaml_data):
    with pytest.raises(ParsingError) as e:
        UnixName(name = yaml_data)
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
