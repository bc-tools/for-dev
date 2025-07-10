#!/usr/bin/env python3

import requests


### TODO
# prototype::
#     content : XXX
#
#     :return: XXX
###
def url_accessible(
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
