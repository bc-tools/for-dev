#!/usr/bin/env python3

from dataclasses  import dataclass
import                   logging
import                   requests
import                   socket
from urllib.parse import urlparse

from aboutmeta.core.constants   import *
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
#     :return: the number of errors detectedwhen validating the
#              URL using DNS and an HTTP technics.
#
#
# note::
#     As the validation system is not 100% reliable, we can
#     only print and log the errors detected (with possible
#     false negatives). This method is best suited for terminal
#     sessions.
###
    def validate(self) -> int:
        url    = self.std
        nb_pbs = 0

# Is DNS resolvable?
        try:
            hostname = urlparse(url).hostname

            logging.info(f"DNS -> {url}")

            socket.gethostbyname(hostname)

            logging.info("Testing hostname OK.")

        except Exception as e:
            nb_pbs += 1

            logging.info("Testing hostname KO!")

            logging.error(
                f"INVALID URL: DNS FAILED for ''{url}'' with "
                f"the following error message.\n{e}"
            )

# Is HTTP valid?
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

# Tests finished.
        return nb_pbs
