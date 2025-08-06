#!/usr/bin/env python3

from typing import List

from dataclasses import dataclass
import                  logging
import                  requests

from email_validator import validate_email

from aboutmeta.core.dataprinter import *


# ----------------------- #
# -- PERSON DATA CLASS -- #
# ----------------------- #

###
# prototype::
#     std         : the person's complete identity with minimal
#                   space used.
#     firstnames  : the list of first names (that can be an empty
#                   list).
#     surname     : the surname which is the only mandatory value.
#     email       : the email adress, or ''None'' if no email
#                   provided.
#     affiliation : the affiliation adress, or ''None'' if no
#                   affiliation provided.
###
@dataclass(frozen = True)
class Person(DataPrinter):
    std        : str
    firstnames : List[str]
    surname    : str
    email      : str | None
    affiliation: str | None

###
# prototype::
#     :return: the only nomralization processe don concern the email adresss.
#
#
# note::
#     Some valid emails adresses use typographical quirks. For example, ``SuPpOrT@OpeAI.CoM`` is valid, but its normalized version, produced by this method, is ``XXXX``.
###
    def normalized(self) -> str:
        email = self._normalized_email(self.email)

        return email

###
# prototype::
#     :return: the only nomralization processe don concern the
#              email adresss.
#
#
# note::
#     Some valid emails adresses use typographical quirks. For
#     example, ``support@OpenAI.CoM`` is valid, but its normalized
#     version, produced by this method, is ``support@openai.com``.
#
#
# caution::
#     According to RFC 5321, we have:
#         + The domain part is case-insensitive, and should be
#         lowercase.
#         + The local part ***may** be case-sensitive, but rarely
#         is.
###
    def _normalized_email(
        self,
        email: str | None
    ) -> str | None:
# Nothing to do.
        if email is None:
            return email

# Let's normalize the email.
        local_part, _, domain_part = email.partition('@')

        normalized_email = f"{local_part}@{domain_part.lower()}"

        return normalized_email




###
# prototype::
#     :return: the number of errors by the validation process
#              of email and membership addresses.
#
#
# note::
#     Since the validation system is not `100%` reliable, we
#     can only print and record the errors detected in a log
#     file with possible false negatives. This method is
#     suitable for terminal sessions.
###
    def validate(self) -> int:
        nb_pbs  = self._validate_email()
        nb_pbs += self._validate_affiliation()

        return nb_pbs

###
# prototype::
#     :return: the number of errors by the validation process
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
#     :return: the number of errors by the validation process
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
# GOOD
    print("----------")
    print("GOOD CASES")
    print("----------")

    someone = Person(
        std         = "A, B, C [support@OpenAI.CoM] (Université de la Technologie, France)",
        firstnames  = ["A", "B"],
        surname     = "C",
        email       = "support@OpenAI.CoM",
        affiliation = "Université de la Technologie, France"
    )

    print()
    print(f"--> {someone.std}")
    print(f"  + Normalized version = {someone.normalized()}")

    print(f"  + Nb pbs = {someone.validate()}")

# BAD
    exit()

    print()
    print("---------")
    print("BAD CASES")
    print("---------")

    someone = Person(
        std         = "A, B, C [support@openaicom] (Université de la Techlogie, France)",
        firstnames  = ["A", "B"],
        surname     = "C",
        email       = "support@openaicom",
        affiliation = "Université de la Techlogie, France"
    )

    print()
    print(f"{someone.std}")
    print(f"  + Nb pbs = {someone.validate()}")
