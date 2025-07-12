#!/usr/bin/env python3

import requests


# ------------------------- #
# -- XXXX -- #
# ------------------------- #

### TODO
# prototype::
#     content : XXX
#
#     :return: XXX
###
def is_url_on_dns(
    url,
    timeout         = 3,
    allow_redirects = True
):
    try:
        response = requests.head(
            url,
            timeout         = 3,
            allow_redirects = True
        )

        return response.status_code < 400

    except requests.RequestException:
        return False
