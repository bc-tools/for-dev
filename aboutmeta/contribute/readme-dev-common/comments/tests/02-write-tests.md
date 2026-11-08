##### Write tests

To be able to run tests by simply invoking the `python` command, tests must rely at least on the following imports.


~~~python
from hypothesis import (
    given,
    strategies as st
)

import pytest

from aboutmeta.core.errors import YAMLTypeError
~~~


Let's explain the design choices made before walking through a concrete example below.

  1. The `given` decorator combined with the strategies provided by `st` allows defining test functions that take arguments yet can be executed without arguments.

  1. `pytest` allows to test that a given exception is properly raised.

  1. Among the tests, there should always be one verifying that non-string input is correctly detected.


The following contribution code snippet demonstrates how to set up the tools described above.


<!-- TESTS (NORMALIZE + ILLEGAL YAML) - URL EXTRACT - START -->

~~~python
# Extract of 'contribute/api/data/code/url.py' (2026-11-08).

# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == '__main__':
    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

    from aboutmeta.core.errors import YAMLTypeError

    ...

# -- Normalized URL -- #
    @given(
        full_data = st.sampled_from([
            (
                'HTTPS://QwAnT.com',
                'https://qwant.com'
            ),
            ...
        ]),
    )
    def test_normalized_URL(full_data):
        yaml_data, std_url = full_data

        mydata = URL(url = yaml_data)
        mydata.normalize()

        assert mydata.url == std_url

    test_normalized_URL()

# -- Illegal YAML data type -- #
    @given(
        yaml_data = st.sampled_from([
            None,
            123,
        ]),
    )
    def test_illegal_yaml_data_type(yaml_data):
        with pytest.raises(YAMLTypeError) as e:
            URL(url = yaml_data)

    test_illegal_yaml_data_type()
~~~

<!-- TESTS (NORMALIZE + ILLEGAL YAML) - URL EXTRACT - END -->


The contribution integration process will generate a test file, similar to the example above, as part of the final test suite. Notice how magic comments like `# -- Magic comment -- #` are formatted, as well as the removal of calls to test functions.


<!-- FINAL UNIT TESTS - URL EXTRACT - START -->

~~~python
# Extract of 'tests/api/data/contribute/test_url.py' (2026-11-08).

import pytest

from aboutmeta.core.errors import YAMLTypeError

...

# -------------------- #
# -- Normalized URL -- #
# -------------------- #

@given(
    full_data = st.sampled_from([
        (
            'HTTPS://QwAnT.com',
            'https://qwant.com'
        ),
        ...
    ]),
)
def test_normalized_URL(full_data):
    yaml_data, std_url = full_data

    mydata = URL(url = yaml_data)
    mydata.normalize()

    assert mydata.url == std_url


# ---------------------------- #
# -- Illegal YAML data type -- #
# ---------------------------- #

@given(
    yaml_data = st.sampled_from([
        None,
        123,
    ]),
)
def test_illegal_yaml_data_type(yaml_data):
    with pytest.raises(YAMLTypeError) as e:
        URL(url = yaml_data)
~~~

<!-- FINAL UNIT TESTS - URL EXTRACT - END -->
