#!/usr/bin/env python3

import requests


# ----------------- #
# -- TEXT ONLINE -- #
# ----------------- #

###
# prototype::
#     url : a URL pointing to an online text file.
#
#     :return: the text of the file found online.
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
            raise FileNotFoundError(f"see URL (404 error):\n{url}")

        else:
            raise RuntimeError(
                f"HTTP error {response.status_code}. "
                f"See URL:\n{url}"
            )

    except requests.exceptions.RequestException as e:
        raise e

# Success implies the return the text (and not the space cowboy).
    return text
