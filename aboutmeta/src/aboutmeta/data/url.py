#!/usr/bin/env python3

from typing import List

from dataclasses  import dataclass
import                   requests
import                   socket
from urllib.parse import urlparse

from .constants  import *

import logging

# -------------------- #
# -- URL DATA CLASS -- #
# -------------------- #

###
# Easy-to-use data class for URLs.
###
@dataclass
class URL:
    url: str

###
# The string representation is be a normalized version using
# the syntax of the path::''about.yaml''.
###
    def __str__(self) -> str:
        return self.url

###  TODO
# prototype::
#     :return: the number of errors detected.
#
# note::
#     As the validation system is not 100% reliable, we can
#     only return a list of errors detected (with possible
#     false negatives). This choice also allows us to produce
#     a final report of everything that has not been validated,
#     thus saving the user from having to spend time studying
#     problems one by one.
###
    def validate(self) -> int:
        url    = self.url
        nb_pbs = 0

# Is DNS resolvable?
        try:
            hostname = urlparse(url).hostname

            logging.info(f"DNS -> {url}")

            socket.gethostbyname(hostname)

            logging.info( "       Testing hostname OK.")

        except Exception as e:
            nb_pbs += 1

            logging.info( "       Testing hostname KO!")

            logging.error(
                f"DNS FAILED for ''{url}'' with following "
                f"SOCKET error message.\n{e}"
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
                logging.info("        Head status OK.")

            else:
                nb_pbs += 1

                logging.info("        Head status KO!")

                logging.error(
                    f"HTTP FAILED for ''{url}'' with following "
                    f"REQUESTS STATUS CODE {response.status_code}."
                )

        except requests.RequestException as e:
            nb_pbs += 1

            logging.info("        Head status KO!")

            logging.error(
                f"HTTP FAILED for ''{url}'' with following "
                f"REQUESTS error message.\n{e}"
            )

# Tests finished.
        return nb_pbs
