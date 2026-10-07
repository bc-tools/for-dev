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
#     yaml_val : the user-input data coming from an `about.yaml`
#                file.
#     url      : a URL.
###
class URL(DataManager):
    yaml_val: str
    url     : str

###
# prototype::
#     :action: a standard URL is built.
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
#     :action: URL validation using DNS and HTTP technics.
###
    def validate(self) -> None:
        self.data_pb.start()

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
                self.data_pb.new_error(
                    data      = url,
                    error_msg = "No hostname scheme supplied.",
                )

            else:
                socket.gethostbyname(hostname)

                self.data_pb.validated(url)

                return

        except Exception as e:
            self.data_pb.new_exception(
                data       = url,
                _exception = e,
            )

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
                self.data_pb.new_error(
                    data      = url,
                    error_msg = f"Requests status code = {response.status_code}.",
                )

        except Exception as e:
            self.data_pb.new_exception(
                data       = url,
                _exception = e,
            )

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

        for n, v in vars(mydata).items():
            if n == 'yaml_val':
                continue

            print(f"{n}: {v}")

        print()
        print(f"Validation process")
        mydata.validate()

        for m in mydata._errors_found:
            print(f"    > {m}")
