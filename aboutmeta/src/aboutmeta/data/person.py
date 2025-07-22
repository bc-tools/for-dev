#!/usr/bin/env python3

from typing import List

from dataclasses import dataclass
import                  logging
import                  requests

from email_validator import (
    validate_email,
    EmailNotValidError
)

from .constants  import *


# ----------------------- #
# -- PERSON DATA CLASS -- #
# ----------------------- #

###
# Easy-to-use data class for persons.
###
@dataclass
class Person:
    firstnames : List[str]
    surname    : str
    email      : str
    affiliation: str

###
# The string representation must be a normalized version using
# the syntax of the path::''about.yaml''.
###
    def __str__(self) -> str:
        text = self.surname

        if self.firstnames:
            firstnames = ', '.join(self.firstnames)
            text       = f"{firstnames}, {text}"

        if self.email:
            text += f' {TAG_YAML_EMAIL_OPEN}{self.email}{TAG_YAML_EMAIL_CLOSE}'

        if self.affiliation:
            text += f' {TAG_YAML_AFFILIATION_OPEN}{self.affiliation}{TAG_YAML_AFFILIATION_CLOSE}'

        return text

###
#     :return: the number of errors detected.
#
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
        nb_pbs = 0

# Valid email address?
        if not self.email is None:
            email = self.email

            try:
                logging.info(f"EMAIL -> {email}")

                validate_email(email)

                logging.info("Email OK.")

            except Exception as e:
                nb_pbs += 1

                logging.info("Email KO!")

                logging.error(
                    f"INVALID EMAIL''{email}'' with the following "
                    f"EXCEPTION.\n{e}"
                )

# Valid affiliation?
        if not self.affiliation is None:
            affi = self.affiliation

            try:
                logging.info(f"AFFILIATION -> {affi}")

                response = requests.get(
                    "https://nominatim.openstreetmap.org/search",
                    params = {
                        "q"     : affi,
                        "format": "json",
                        "limit" : 1,
                    },
                    headers = {
                        "User-Agent": "AdresseChecker/1.0"
                    }
                )

                if response.ok and len(response.json()) > 0:
                    logging.info("Affiliation OK.")

                else:
                    nb_pbs += 1

                    logging.info("Affiliation KO!")

                    logging.error(
                        f"INVALID AFFILIATION ''{affi}'': "
                         "nothing found by OPENSTREETMAP."
                    )

            except Exception as e:
                nb_pbs += 1

                logging.info("Affiliation KO!")

                logging.error(
                    f"INVALID AFFILIATION ''{affi}'' with the following "
                    f"EXCEPTION.\n{e}"
                )

# Tests finished.
        return nb_pbs
