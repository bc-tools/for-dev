#!/usr/bin/env python3

import logging
import requests

from email_validator import validate_email

from aboutmeta.core.constants    import *
from aboutmeta.core.data_manager import (
    DataManager,
    DataPB
)

from aboutmeta.tools.misc  import (
    no_space_around,
    single_spaces
)

# ----------------------- #
# -- PERSON DATA CLASS -- #
# ----------------------- #

###
# prototype::
#     firstnames  : the list of first names (that can be an empty
#                   list).
#     surname     : the surname consists of an optional particle,
#                   with the special value ''None'' indicating its
#                   absence, and a mandatory main surname, which
#                   is required for any person record.
#     email       : the email adress, or ''None'' if no email
#                   provided.
#     affiliation : the affiliation adress, or ''None'' if no
#                   affiliation provided.
###
class Person(DataManager):
    firstnames : list[str]
    surname    : tuple[str | None, str]
    email      : str | None
    affiliation: str | None

###
# prototype::
#     :action: the normalization process concern firstnames,
#              surname, and email adress.
#
#     :see: self._normalize_titles,
#           self._normalize_email,
#           self._normalize_affiliation
#
#
# Here are the normalizations performed.
#
#     + All names are written in "titlecase", and the particle
#     is in lowercase. Spaces around the hyphen are removed.
#     For example,
#     ''ALIce,  MarIE   -  LiSe,   {DE}   Charlène'' becomes
#     ''Alice,  Marie-Lise, {de} Charlène''.
#
#     + Some valid emails adresses use typographical quirks.
#     For example, ''SuPpOrT@OpeAI.CoM'' is valid, but its
#     normalized version, produced by this method, is
#     ''SuPpOrT@openai.com''. See the ''_normalize_email''
#     method for technical details.
#
#     + The normalization of the affiliation address is limited
#     to not having consecutive spaces.
#     For example,
#     ''Université   de   la Technologie,    France'' becomes
#     ''Université de la Technologie, France''.
###
    def normalize(self) -> None:
        self._normalize_titles()
        self._normalize_email()
        self._normalize_affiliation()

###
# prototype::
#     :action: all names are written in "titlecase", and the
#              particle is in lowercase.
#
#     :see: self._normalize_name
###
    def _normalize_titles(self) -> None:
# First names.
        self.firstnames = map(
            self._normalize_name,
            self.firstnames
        )

# Particle?
        if not self.surname[0] is None:
            self.surname[0] = self.surname[0].lower()

# Main name.
        self.surname[1] = self._normalize_name(self.surname[1])

###
# prototype::
#     name : a name to be normalized.
#
#     :return: name in "titlecase" without unnecessary spaces.
###
    def _normalize_name(
        self,
        name: str
    ) -> str:
        name = single_spaces(name)
        name = name.title()
        name = no_space_around(
            text = name,
            part = '-'
        )

        return name

###
# prototype::
#     :action: email is normalized according to RFC 5321.
#
#
# caution::
#     According to RFC 5321, we have:
#
#         + The domain part is case-insensitive, and should
#         be lowercase.
#
#         + The local part ***may*** be case-sensitive, but
#         rarely is.
###
    def _normalize_email(self) -> None:
# Nothing to do.
        if self.email is None:
            return

# Let's normalize the email.
        local_part, _ , domain_part = self.email.partition('@')

        self.email = f"{local_part}@{domain_part.lower()}"

###
# prototype::
#     :action: unnecessary spaces are rempved from the
#              affiliation adresss.
###
    def _normalize_affiliation(self) -> None:
# Nothing to do.
        if self.affiliation is None:
            return

# Let's normalize the affiliation.
        self.affiliation = single_spaces(affiliation)






###
# prototype::
#     :return: the number of errors found by the validation
#              process of email and membership addresses.
#
#     :see: self._validate_email,
#           self._validate_affiliation
#
#
# important::
#     Since the validation system is not `100%` reliable, we
#     can only print and record the errors detected in a log
#     file with possible false negatives. This method is
#     suitable for terminal sessions.
###
    def validate(self) -> DataPB:
        data_pb = DataPB(self)

        self._validate_email(data_pb)
        self._validate_affiliation(data_pb)

        return data_pb

###
# prototype::
#     :return: the number of errors found by the validation
#              process of the email address.
###
    def _validate_email(
        self,
        data_pb: DataPB
    ) -> None:
        if self.email is None:
            return data_pb

        email = self.email

        try:
            data_pb.what(
                desc  = "EMAIL"
                value = email
            )

            validate_email(email)

            data_pb.success()

        except Exception as e:
            data_pb.failure(
                f"INVALID EMAIL''{email}'' with the following "
                f"EXCEPTION.\n{e}"
            )

        return nb_pbs

###
# prototype::
#     :return: the number of errors found by the validation
#              process of the affiliation address.
###
    def _validate_affiliation(
        self,
        data_pb: DataPB
    ) -> None:
        nb_pbs = 0

        if self.affiliation is None:
            return nb_pbs

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


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print("----------")
    print("GOOD CASES")
    print("----------")

    someone = Person(
        firstnames  = ["ALIce", "MarIE  -  LiSe"],
        surname     = ("DE", "Charlène"),
        email       = "support@OpenAI.CoM",
        affiliation = "Université   de   la Technologie,    France"
    )

    print("someone - BEFORE")
    print(someone)

    someone.normalize()

    print("someone - AFTER")
    print(someone)

    print(f"Nb validation pbs = {someone.validate()}")

# BAD
    exit()

    print()
    print("---------")
    print("BAD CASES")
    print("---------")

    someone = Person(
        firstnames  = ["A", "B"],
        surname     = "C",
        email       = "support@openaicom",
        affiliation = "Université de la Techlogie, France"
    )

    print()
    print(f"  + Nb validation pbs = {someone.validate()}")
