#!/usr/bin/env python3

from typing import List

from dataclasses import dataclass
import                  logging
import                  requests

from email_validator import validate_email

# from aboutmeta.core.constants   import *
from aboutmeta.core.dataprinter import *


# ----------------------- #
# -- PERSON DATA CLASS -- #
# ----------------------- #

###
# prototype::
#     std        : the person's complete identity with minimal space
#                  used.
#     firstnames : the list of first names.
#     surname    : the surname.
#     email      : the email adress.
#     affiliation: the affiliation adress.
###
@dataclass(frozen = True)
class Person(DataPrinter):
    std        : str
    firstnames : List[str]
    surname    : str
    email      : str
    affiliation: str

###
# prototype::
#     :return: the number of errors detected during the validation
#              of email and membership addresses.
#
#
# note::
#     Since the validation system is not 100% reliable, we can only
#     print and record the errors detected in a log file (with
#     possible false negatives). This method is particularly suitable
#     for terminal sessions.
###
    def validate(self) -> int:
        nb_pbs = self._validate_email() + self._validate_affiliation()

        return nb_pbs

###
# prototype::
#     :return: the number of errors detected during the validation
#              of the email address.
###
    def _validate_email(self) -> int:
        nb_pbs = 0

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

        return nb_pbs

###
# prototype::
#     :return: the number of errors detected during the validation
#              of the affiliation address.
###
    def _validate_affiliation(self) -> int:
        nb_pbs = 0

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
                    f"INVALID AFFILIATION ''{affi}'' with "
                    f"the following EXCEPTION.\n{e}"
                )

        return nb_pbs


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
    someone = Person(
        std         = "A, B, C [support@openai.com] (Université de la Technologie, France)",
        firstnames  = ["A", "B"],
        surname     = "C",
        email       = "support@openai.com",
        affiliation = "Université de la Technologie, France"
    )

    print(f"Nb pbs: {someone.validate()}")
