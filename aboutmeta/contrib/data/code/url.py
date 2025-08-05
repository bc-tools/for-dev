#!/usr/bin/env python3

from dataclasses  import dataclass
import                   logging
import                   requests
import                   socket
from urllib.parse import urlparse

from aboutmeta.core.dataprinter import *


# -------------------- #
# -- URL DATA CLASS -- #
# -------------------- #

###
# prototype::
#     std : an url.
###
@dataclass(frozen = True)
class URL(DataPrinter):
    std: str

###
# prototype::
#     :return: the number of errors detected during the validation
#              of the URL using DNS and an HTTP technics.
#
#
# note::
#     Since the validation system is not 100% reliable, we can only
#     print and record the errors detected in a log file (with
#     possible false negatives). This method is particularly suitable
#     for terminal sessions.
###
    def validate(self) -> int:
        nb_pbs  = self._validate_DNS()
        nb_pbs += self._validate_HTTP()

        return nb_pbs

###
# prototype::
#     :return: the number of errors detected during the validation
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
#     :return: the number of errors detected during the validation
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
        "https://google.com",
        "google.com"
    ]:
        print('---')
        print(f"Testing {std}")

        url = URL(std = std)

        print(f"Nb pbs: {url.validate()}")
