##### Write tests

To be able to run tests by simply invoking the `python` command, tests must rely at least on the following imports.


~~~python
from hypothesis import (
    given,
    strategies as st
)

import pytest
~~~


Let's explain the design choices made before walking through a concrete example below.

  1. The `given` decorator combined with the strategies provided by `st` allows defining test functions that take arguments yet can be executed without arguments.

  1. `pytest` allows to test that a given exception is properly raised.


The following contribution code snippet demonstrates how to set up the tools described above.


<!-- TESTS (NORMALIZE + ILLEGAL YAML) - URL EXTRACT - START -->

~~~python
# Extract of 'contribute/api/data/code/url.py' (2026-11-11).

# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == '__main__':
    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

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

# -- Illegal data type -- #
    @given(
        yaml_data = st.sampled_from([
            None,
            123,
        ]),
    )
    def test_illegal_data_type(yaml_data):
        with pytest.raises(TypeError) as e:
            URL(url = yaml_data)

    test_illegal_data_type()
~~~

<!-- TESTS (NORMALIZE + ILLEGAL YAML) - URL EXTRACT - END -->


The contribution integration process will generate a test file, similar to the example above, as part of the final test suite. Notice the formatting of magic comments like `# -- Magic comment -- #`, the removal of test function calls, and the automatic addition of a prefix matching the contribution file.


<!-- FINAL UNIT TESTS - URL EXTRACT - START -->

~~~python
# Extract of 'tests/api/data/contribute/test_url.py' (2026-11-11).

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.data.url import *

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/data/code/url.py'

from hypothesis import (
    given,
    strategies as st
)

import pytest

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


# ----------------------- #
# -- Illegal data type -- #
# ----------------------- #

@given(
    yaml_data = st.sampled_from([
        None,
        123,
    ]),
)
def test_illegal_data_type(yaml_data):
    with pytest.raises(TypeError) as e:
        URL(url = yaml_data)
~~~

<!-- FINAL UNIT TESTS - URL EXTRACT - END -->


> ***CAUTION.*** *If you need multi-line text with content starting at the beginning of the line, use only `'''...'''` or `"""..."""` without chaining any methods directly onto the triple quotes. String method calls must be applied in a second step. This stems from our basic test code integration approach.*
