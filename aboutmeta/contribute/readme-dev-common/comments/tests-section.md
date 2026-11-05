#### 'TESTS' section (mandatory)








XXX


verbeux mais imoser par tests faits en intern, utilser le template



~~~python
# Extract of UnixName class code (2026-11-01).

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
    @given(
        yaml_data = st.sampled_from([
            '_abc-cde123',
        ]),
    )
    def test_legal_name(yaml_data):
        mydata = UnixName(name = yaml_data)

        assert mydata.name == yaml_data

    test_legal_name()


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
~~~


code automatiquement fabriqué : copier coller sans les section dev et les appels des finctions tests, + préfixage des fonctions

~~~python
# Extract of UnixName class unit tests (2026-11-01).

from hypothesis import (
    given,
    strategies as st
)

import pytest

from aboutmeta.core.errors import YAMLTypeError


# ---------------------- #
# -- Legal UNIX names -- #
# ---------------------- #

@given(
    yaml_data = st.sampled_from([
        '_abc-cde123',
    ]),
)
def test_unixname_legal_name(yaml_data):
    mydata = UnixName(name = yaml_data)

    assert mydata.name == yaml_data


# ------------------------ #
# -- Illegal UNIX names -- #
# ------------------------ #

@given(
    yaml_data = st.sampled_from([
        '-hyphen-pb',
        'CasePB',
        '123-digits-pb',
    ]),
)
def test_unixname_illegal_name(yaml_data):
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
