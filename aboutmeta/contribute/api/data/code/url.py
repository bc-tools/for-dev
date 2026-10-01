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
    yaml_val: str
    url     : str

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
        parsed_url = urlparse(self.yaml_val)

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
        self._errors_found = []

        self._validate_DNS()
        self._validate_HTTP()

###
# prototype::
#     :action: DNS check of the hostname.
###
    def _validate_DNS(self) -> None:
        self.data_pb.what("DNS status")

        url = self.url

        try:
            self.data_pb.checking(url)

            hostname = urlparse(url).hostname

            if hostname is None:
                msg = f"{url}: No hostname scheme supplied."

                self.data_pb.error(msg)
                self._errors_found.append(msg)

            else:
                socket.gethostbyname(hostname)

                self.data_pb.validated(url)

                return

        except Exception as e:
            msg = f"'{url}': {e}"

            self.data_pb.exception(msg)
            self._errors_found.append(msg)

        self.data_pb.rejected(url)


###
# prototype::
#     :action: HTTP URL availability check.
###
    def _validate_HTTP(self) -> None:
        self.data_pb.what("HTTP status")

        url = self.url

        try:
            self.data_pb.checking(url)

            response = requests.head(
                url,
                timeout         = 3,
                allow_redirects = True
            )

            if response.status_code < 400:
                self.data_pb.validated(url)

                return

            else:
                msg = f"'{url}': Requests status code = {response.status_code}."

                self.data_pb.error(msg)
                self._errors_found.append(msg)


        except Exception as e:
            msg = f"'{url}': {e}"

            self.data_pb.exception(msg)
            self._errors_found.append(msg)

        self.data_pb.rejected(url)


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from aboutmeta.core.log_conf import *
    setup_logging()

    for url in [
        "HTTPS://QwAnT.com",
        "qwant.com",
        "HTTP://Example.COM/Mon Dôssier/Fichier Testé.html"
    ]:
        print('---')

        mydata = URL(
            yaml_val = url,
            url      = url
        )

        print()
        print("'repr' form")
        print(repr(mydata))

        print()
        print("Original data")
        print(mydata)

        print()
        print("Normalization")
        mydata.normalize()
        print(mydata)

        print()
        print(f"Validation process")
        mydata.validate()
