#!/usr/bin/env python3

import requests


# ----------------- #
# -- TEXT ONLINE -- #
# ----------------- #

###
# prototype::
#     url : XXXX
#
#     :return: the full text of the license downloaded from the SPDX
#              website.
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

# Success implies to return the text.
    return text
