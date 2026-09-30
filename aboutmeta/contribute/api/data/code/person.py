#!/usr/bin/env python3

import requests

from email_validator import validate_email

from aboutmeta.core.data_manager import DataManager

from aboutmeta.tools.misc  import (
    no_space_around,
    single_spaces
)


# ----------------------- #
# -- PERSON DATA CLASS -- #
# ----------------------- #

###
# prototype::
#     surname     : the surname without a particle is mandatory.
#     particle    : the particle of a surname, or ''""'' if no
#                   particle is needed.
#     firstnames  : the list of first names (that can be an empty
#                   list).
#     email       : the email adress, or ''""'' if no email
#                   provided.
#     affiliation : the affiliation adress, or ''""'' if no
#                   affiliation provided.
###
class Person(DataManager):
    yaml_val   : str
    surname    : str
    particle   : str        = ''
    firstnames : tuple[str] = tuple()
    email      : str        = ''
    affiliation: str        = ''

###
# prototype::
#     :action: the normalization process concern firstnames,
#              surname, email adress, and affiliation.
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
#     ''Alice, Marie-Lise, {de} Charlène''.
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
        self.firstnames = tuple(
            map(
                self._normalize_name,
                self.firstnames
            )
        )

# Particle.
        self.particle = self.particle.lower()

# Main name.
        self.surname = self._normalize_name(self.surname)

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
        if self.email:
            local_part, _ , domain_part = self.email.partition('@')

            self.email = f"{local_part}@{domain_part.lower()}"

###
# prototype::
#     :action: unnecessary spaces are removed from the
#              affiliation adresss.
###
    def _normalize_affiliation(self) -> None:
        if self.affiliation:
            self.affiliation = single_spaces(self.affiliation)

###
# prototype::
#     :action: email and affiliation checking.
#
#     :see: self._validate_email,
#           self._validate_affiliation
###
    def validate(self) -> None:
        self._validate_email()
        self._validate_affiliation()

###
# prototype::
#     :action: ''email_validator.validate_email'' checks the email
#              validity.
###
    def _validate_email(self) -> None:
        self.data_pb.what("EMAIL")

# Nothing to do.
        if not self.email:
            self.data_pb.msg(f"No email.")

            return

# Let's validate the email.
        email = self.email

        try:
            self.data_pb.msg(f"Checking {email}")

            validate_email(email)

            self.data_pb.success()

        except Exception as e:
            self.data_pb.exception(e)

###
# prototype::
#     :action: OpenStreetMap verifies the affiliation.
###
    def _validate_affiliation(self) -> None:
        self.data_pb.what("AFFILIATION")

# Nothing to do.
        if not self.affiliation:
            self.data_pb.msg(f"No affiliation.")

            return

# Let's validate the affiliation.
        affi = self.affiliation

        try:
            self.data_pb.msg(f"Checking {affi}")

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
                self.data_pb.success()

            else:
                self.data_pb.failure(
                    "OPENSTREETMAP: nothing found."
                )

        except Exception as e:
            self.data_pb.exception(e)


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from aboutmeta.core.log_conf import *

    setup_logging()

# GOOD
    print("----------")
    print("GOOD CASES")
    print("----------")

    mydata = Person(
        yaml_val    = (
            "ALIce, MarIE  -  LiSe, "
            "DE Charlène [support@OpenAI.CoM] "
            "(Université   de   la Technologie,    France)"
        ),
        firstnames  = ["ALIce", "MarIE  -  LiSe"],
        particle    = "DE",
        surname     = "Charlène",
        email       = "support@OpenAI.CoM",
        affiliation = "Université   de   la Technologie,    France"
    )

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

# BAD
    # exit()

    print()
    print("---------")
    print("BAD CASES")
    print("---------")

    mydata = Person(
        yaml_val    = (
            "A, B, C [support@openaicom] "
            "(Université de la Techlogie, France)"
        ),
        firstnames  = ["A", "B"],
        surname     = "C",
        email       = "support@openaicom",
        affiliation = "Université de la Techlogie, France"
    )

    print("Original data")
    print(mydata)

    print()
    print(f"Validation process")
    mydata.validate()
