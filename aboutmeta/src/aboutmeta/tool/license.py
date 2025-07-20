#!/usr/bin/env python3

import requests


# --------------- #
# -- CONSTANTS -- #
# --------------- #

URL_TEMPL_SPDX_LICENSE_TEXT = (
    "https://raw.githubusercontent.com/spdx/"
    "license-list-data/main/text/{}.txt"
)


# ------------------ #
# -- LICENSE TEXT -- #
# ------------------ #

###
# prototype::
#     license_id : an SPDX license code.
#
#     :return: the fule text of the license.
###
def get_licence_text(license_id: str) -> str:
# Let's try to get the text.
    try:
        response = requests.get(
            url     = URL_TEMPL_SPDX_LICENSE_TEXT.format(license_id),
            timeout = 5
        )

        if response.status_code == 200:
            text = response.text

        elif response.status_code == 404:
            raise FileNotFoundError(
                f"bad SPDX_ID:\n{license_id}"
            )

        else:
            raise RuntimeError(
                f"HTTP error {response.status_code}. URL used:\n"
                f"{response.url}"
            )

    except requests.exceptions.RequestException as e:
        raise e

# Success implies returned text.
    return text
