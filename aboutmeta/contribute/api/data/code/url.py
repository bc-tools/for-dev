#!/usr/bin/env python3

import httpx
import socket

from urllib.parse import (
    quote as urlquote,
    urlparse,
    urlunparse,
)


from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError
from aboutmeta.core.validate     import validate_type


# ---------- #
# -- DATA -- #
# ---------- #

###
# prototype::
#     url: a \url.
###
class URL(DataManager):
    url: str

###
# prototype::
#     :action: mandatory validation of ''self.URL'' type.
###
    def __post_init__(self) -> None:
        validate_type(
            data_name      = 'URL',
            data           = self.url,
            types_expected = str,
        )

        self.url = self.url.strip()

###
# prototype::
#     :action: a standard ''URL'' object is built.
#
#
# Here are the normalizations done.
#
#     1. Some valid \urls use typographical quirks. For example,
#     ''HTTPS://QwAnT.com'' is valid, but its normalized version
#     is ''https://qwant.com''.
#
#     1. Special \html character encoding is also handled. For
#     example, ''http://abc.com/Dôssier Testé.html'' becomes
#     ''http://abc.com/D%C3%B4ssier%20Test%C3%A9.html''.
###
    def normalize(self) -> None:
        parsed_url = urlparse(self.url)

        self.url = urlunparse((
            parsed_url.scheme,                     # http, https
            parsed_url.netloc.lower(),             # Domain
            # parsed_url.path,                     # No HTML encoding!
            urlquote(parsed_url.path, safe = '/'), # HTML encoding
            parsed_url.params,                     # Keep params.
            parsed_url.query,                      # Keep query string.
            parsed_url.fragment                    # Keep fragment (#...).
        ))

###
# prototype::
#     :action: \url validation using \dns and \http \techs.
###
    def validate(self) -> None:
        self.data_pb.start()

        self._validate_DNS()
        self._validate_HTTP()

###
# prototype::
#     :action: \dns check of the hostname.
###
    def _validate_DNS(self) -> None:
        self.data_pb.what('DNS status')

        url = self.url

        try:
            self.data_pb.checking(url)

            hostname = urlparse(url).hostname

            if hostname is None:
                self.data_pb.new_error(
                    data      = url,
                    error_msg = 'No hostname scheme supplied.',
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
#     :action: \http \url availability check.
###
    def _validate_HTTP(self) -> None:
        self.data_pb.what('HTTP status')

        url = self.url

        try:
            self.data_pb.checking(url)

            response = httpx.head(
                url,
                timeout          = 3,
                follow_redirects = True
            )

            if response.status_code < 400:
                self.data_pb.validated(url)

                return

            else:
                self.data_pb.new_error(
                    data      = url,
                    error_msg = f'HTTPX status code = {response.status_code}.',
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

if __name__ == '__main__':
# dev:
    INTERACTIVE_SESSION = True
    INTERACTIVE_SESSION = False
# :dev

    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

    from aboutmeta.core.errors import YAMLTypeError

# dev:
    if INTERACTIVE_SESSION:
        from aboutmeta.core.log_conf import *

        setup_logging()

        for yaml_data in [
            # Good cases.
            'HTTPS://QwAnT.com   ',
            # Bad cases.
            'qwant.com',
            'HTTP://Example.COM/Mon Dôssier/Fichier Testé.html',
        ]:
            mydata = URL(url = yaml_data)

            print("---")
            print(f'{yaml_data = }')
            print(f'{mydata    = }')

            print()
            print('Normalization')
            mydata.normalize()
            print(f'{mydata = }')

            print()
            print('Validation process')
            print(f'{mydata = }')

            mydata.validate()

            for m in mydata._errors_found:
                print(f'    > {m}')

        exit()
# :dev

# -- Legal URL -- #
    @given(
        yaml_data = st.sampled_from([
            'HTTPS://QwAnT.com',
            'qwant.com',
            'HTTP://Example.COM/Mon Dôssier/Fichier Testé.html',
        ]),
    )
    def test_legal_URL(yaml_data):
        mydata = URL(url = yaml_data)

        assert mydata.url == yaml_data

    test_legal_URL()

# -- Normalized URL -- #
    @given(
        full_data = st.sampled_from([
            (
                'HTTPS://QwAnT.com',
                'https://qwant.com'
            ),
            (
                'qwant.com',
                'qwant.com'
            ),
            (
                'HTTP://Example.COM/Mon Dôssier/Fichier Testé.html',
                'http://example.com/Mon%20D%C3%B4ssier/Fichier%20Test%C3%A9.html'
            ),
        ]),
    )
    def test_normalized_URL(full_data):
        yaml_data, std_url = full_data

        mydata = URL(url = yaml_data)
        mydata.normalize()

        assert mydata.url == std_url

    test_normalized_URL()

# -- Illegal YAML data type -- #
    @given(
        yaml_data = st.sampled_from([
            None,
            123,
        ]),
    )
    def test_illegal_yaml_data_type(yaml_data):
        with pytest.raises(YAMLTypeError) as e:
            URL(url = yaml_data)

# dev:
        print('---')
        print(f'{yaml_data = }')
        print(e)
# :dev

    test_illegal_yaml_data_type()
