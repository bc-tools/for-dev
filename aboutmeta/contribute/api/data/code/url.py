#!/usr/bin/env python3

import requests
import socket

from urllib.parse import (
    quote,
    urlparse,
    urlunparse,
)

from aboutmeta.core.data_manager import DataManager


# -------------------- #
# -- URL DATA CLASS -- #
# -------------------- #

###
# prototype::
#     url : a URL.
###
class URL(DataManager):
    url: str

###
# prototype::
#     :action: a standard URL is build.
#
#
# Here are the normalizations done.
#
#     1. Some valid URLs use typographical quirks.
#     For example, ''HTTPS://QwAnT.com'' is valid, but its
#     normalized version is ''https://qwant.com''.
#
#     1. Special HTML character encoding is also handled.
#     For example, ''http://abc.com/Dôssier Testé.html''
#     becomes ''http://abc.com/D%C3%B4ssier%20Test%C3%A9.html''.
###
    def normalize(self) -> None:
        parsed_url = urlparse(self.std_value)

        self.url = urlunparse((
            parsed_url.scheme,          # http, https
            parsed_url.netloc.lower(),  # Domain
            # parsed_url.path,            # No HTML encoding!
            quote(parsed_url.path, safe="/"), # HTML encoding
            parsed_url.params,          # Keep params.
            parsed_url.query,           # Keep query string.
            parsed_url.fragment         # Keep fragment (#...).
        ))

###
# prototype::
#     :action: URL check using DNS and HTTP technics.
###
    def validate(self) -> None:
        self._validate_DNS()
        self._validate_HTTP()

###
# prototype::
#     :action: DNS check of the hostname.
###
    def _validate_DNS(self) -> None:
        self.data_pb.what("DNS")

        url = self.url

        try:
            self.data_pb.msg(f"Checking {url}")

            hostname = urlparse(url).hostname

            if hostname is None:
                self.data_pb.failure("No hostname scheme supplied.")

            else:
                socket.gethostbyname(hostname)

                self.data_pb.success()

        except Exception as e:
            self.data_pb.exception(e)

###
# prototype::
#     :action: HTTP URL availability check.
###
    def _validate_HTTP(self) -> None:
        self.data_pb.what("HTTP STATUS")

        url = self.url

        try:
            self.data_pb.msg(f"Checking {url}")

            response = requests.head(
                url,
                timeout         = 3,
                allow_redirects = True
            )

            if response.status_code < 400:
                self.data_pb.success()

            else:
                self.data_pb.failure(
                    f"REQUESTS STATUS CODE: {response.status_code}."
                )

        except Exception as e:
            self.data_pb.exception(e)


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    for url in [
        "HTTPS://QwAnT.com",
        "qwant.com",
        "HTTP://Example.COM/Mon Dôssier/Fichier Testé.html"
    ]:
        print('---')

        mydata = URL(url = url)

        print("Original data")
        print(mydata)

        print("Normalization")
        mydata.normalize()
        print(mydata)

        print(f"Validation process")
        mydata.validate()
