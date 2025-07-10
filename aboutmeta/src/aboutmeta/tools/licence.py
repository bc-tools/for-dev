#!/usr/bin/env python3

import requests


# --------------- #
# -- CONSTANTS -- #
# --------------- #

URL_TEMPL_SPDX_LICENSE_TEXT = (
    "https://raw.githubusercontent.com/spdx/"
    "license-list-data/main/text/{}.txt"
)


# ------------------------- #
# -- XXXX -- #
# ------------------------- #

###
# prototype::
#     license_id : XXX
#
#     :return: XXX
###
def get_licence_text(license_id):
    try:
        response = requests.get(
            url     = URL_TEMPL_SPDX_LICENSE_TEXT.format(license_id),
            timeout = 5
        )

        if response.status_code == 200:
            text = response.text

        elif response.status_code == 404:
            raise FileNotFoundError(
                f"aboutmeta BUG!\nBad SPDX_URL:\n{lic_url}"
            )

        else:
            raise RuntimeError(
                f"HTTP error {response.status_code}."
            )

    except requests.exceptions.RequestException as e:
        raise e

    return text
