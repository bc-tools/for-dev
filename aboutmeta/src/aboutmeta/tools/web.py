#!/usr/bin/env python3

import requests


# ----------------- #
# -- TEXT ONLINE -- #
# ----------------- #

###
# prototype::
#     url : \url pointing to an online text file.
#
#     :return: file text content found online.
###
def get_text_from(url: str) -> str:
# Let's try to get the text.
    try:
        response = requests.get(
            url     = url,
            timeout = 5
        )

        if response.status_code == 200:
            text = response.text

        elif response.status_code == 404:
            raise FileNotFoundError(
                f"404 error. "
                f"See URL:\n{url}"
            )

        else:
            raise RuntimeError(
                f"HTTP error {response.status_code}. "
                f"See URL:\n{url}"
            )

    except requests.exceptions.RequestException as e:
        raise e

# Success implies the return the text (and not the space cowboy).
    return text


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from hypothesis import (
        given,
        settings, # Cf coverage tests.
        strategies as st
    )

    import pytest

# -- Legal spec -- #
    @settings(deadline = None) # Cf coverage tests.
    def test_legal_url() -> None:
        get_text_from('https://httpbin.org/robots.txt')

    test_legal_url()

# -- 404 HTTP error -- #
    @settings(deadline = None) # Cf coverage tests.
    def test_404_HTTP_error() -> None:
        with pytest.raises(FileNotFoundError) as e:
            get_text_from('https://httpbin.org/robos.txt')

    test_404_HTTP_error()

# -- None 404 HTTP error -- #
    @settings(deadline = None) # Cf coverage tests.
    @given(
        url = st.sampled_from([
            'https://bidon.org/non.txt',
        ]),
    )
    def test_none_404_HTTP_error(url: str) -> None:
        with pytest.raises(RuntimeError) as e:
            get_text_from(url)

    test_none_404_HTTP_error()
