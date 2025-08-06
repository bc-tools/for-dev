#!/usr/bin/env python3

from dataclasses  import dataclass
import                   logging
import                   requests
import                   socket
from urllib.parse import (
    urlparse,
    urlunparse,
)

from aboutmeta.core.dataprinter import DataPrinter


# -------------------- #
# -- URL DATA CLASS -- #
# -------------------- #

###
# prototype::
#     std : an url (no processing has been performed, the URL
#           is recorded verabtim).
###
@dataclass(frozen = True)
class URL(DataPrinter):
    std: str

###
# prototype::
#     :return: a normalized version of the URL.
#
#
# Some valid URLs use typographical quirks. For example,
# ''HTTPS://QwAnT.com'' is valid, but its normalized version,
# produced by this method, is ''https://qwant.com''.
# However, this method doesn't handle the HTML encoding of
# special characters. For example,
# ''http://example.com/Dôssier Testé.html''
# doesn't become
# ''http://example.com/D%C3%B4ssier%20Test%C3%A9.html''.
# This will produce human-readable path::''about.yaml'' files.
###
    def normalized(self) -> str:
        parsed_url = urlparse(self.std)

        norm_url = urlunparse((
            parsed_url.scheme,          # http, https
            parsed_url.netloc.lower(),  # Domain
            parsed_url.path,            # No HTML encoding!
            parsed_url.params,          # Keep params.
            parsed_url.query,           # Keep query string.
            parsed_url.fragment         # Keep fragment (#...).
        ))

        return norm_url

###
# prototype::
#     :return: the number of errors by the validation process
#              of the URL using DNS and an HTTP technics.
#
#
# important::
#     Since the validation system is not `100%` reliable, we
#     can only print and record the errors detected in a log
#     file with possible false negatives. This method is
#     suitable for terminal sessions.
###
    def validate(self) -> int:
        nb_pbs  = self._validate_DNS()
        nb_pbs += self._validate_HTTP()

        return nb_pbs

###
# prototype::
#     :return: the number of errors by the validation process
#              of the URL using DNS technics.
###
    def _validate_DNS(self) -> int:
        url    = self.std
        nb_pbs = 0

        try:
            logging.info(f"DNS -> {url}")

            hostname = urlparse(url).hostname

            if hostname is None:
                nb_pbs += 1

                logging.info("Testing hostname KO!")
                logging.error("No scheme supplied.")


            else:
                socket.gethostbyname(hostname)

                logging.info("Testing hostname OK.")

        except Exception as e:
            nb_pbs += 1

            logging.info("Testing hostname KO!")
            logging.error(
                f"INVALID URL: DNS FAILED for ''{url}'' with "
                f"the following error message.\n{e}"
            )

        return nb_pbs

###
# prototype::
#     :return: the number of errors by the validation process
#              of the URL using HTTP technics.
###
    def _validate_HTTP(self) -> int:
        url    = self.std
        nb_pbs = 0

        try:
            logging.info(f"HTTP -> {url}")

            response = requests.head(
                url,
                timeout         = 3,
                allow_redirects = True
            )

            if response.status_code < 400:
                logging.info(" Head status OK.")

            else:
                nb_pbs += 1

                logging.info(" Head status KO!")
                logging.error(
                    f"INVALID URL: HTTP FAILED for ''{url}'' with "
                    f"the REQUESTS STATUS CODE {response.status_code}."
                )

        except Exception as e:
            nb_pbs += 1

            logging.info(" Head status KO!")
            logging.error(
                f"INVALID URL: HTTP FAILED for ''{url}'' with "
                f"the following EXCEPTION.\n{e}"
            )

        return nb_pbs


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
    for std in [
        "HTTPS://QwAnT.com",
        "qwant.com",
        "HTTP://Example.COM/Mon Dôssier/Fichier Testé.html"
    ]:
        print('---')
        print(f"Testing {std}")

        url = URL(std = std)

        print(f"NORMALIZED: {url.normalized()}")

        nb_pbs = url.validate()

        print(f"NB PBS: {url.validate()}")
