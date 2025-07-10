#!/usr/bin/env python3

import requests

###
# prototype::
#     license_id : XXX
#
#     :return: XXX
###
def get_licence_text(license_id):
    lic_url = f"https://raw.githubusercontent.com/spdx/license-list-data/main/text/{license_id}.txt"

    try:
        response = requests.get(
            url     = lic_url,
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
