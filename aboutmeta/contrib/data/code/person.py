#!/usr/bin/env python3

import                  logging
import                  requests

from email_validator import validate_email

from aboutmeta.core.constants   import *
from aboutmeta.core.dataprinter import (
    dataclass,
    DataPrinter
)
from aboutmeta.tool.group import gather_groups
from aboutmeta.tool.misc  import (
    no_space_around,
    single_spaces
)


# ----------------------- #
# -- PERSON DATA CLASS -- #
# ----------------------- #

###
# prototype::
#     std         : the person's complete identity with minimal
#                   space used.
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
#
#
# note::
#     The ''std'' attribute is part of the frozen dataclass
#     ''DataPrinter''.
###
@dataclass(frozen = True)
class Person(DataPrinter):
    firstnames : list[str]
    surname    : tuple[str | None, str]
    email      : str | None
    affiliation: str | None

###
# prototype::
#     :return: the normalization process concern firstnames,
#              surname, and email adress.
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
#     ''SuPpOrT@openai.com''. See the ''_normalized_email''
#     method for technical details.
#
#     + The normalization of the affiliation address is limited
#     to not having consecutive spaces.
#     For example,
#     ''Université   de   la Technologie,    France'' becomes
#     ''Université de la Technologie, France''.
###
    def normalized(self) -> str:
        titles = self._normalized_titles()

        email = (
            ""
            if self.email is None else
            self._normalized_email()
        )

        affiliation = (
            ""
            if self.affiliation is None else
            self._normalized_affiliation()
        )

        norm_person = gather_groups(
            groups = [titles, email, affiliation],
            delims = DELIMS_PERSON,
        )

        return norm_person

###
# prototype::
#     :return: the CSV list of names in "titlecase", except the
#              particle which is lowercase.
###
    def _normalized_titles(self) -> str:
# First names.
        titles = [
            self._normalized_name(n)
            for n in self.firstnames
        ]

# Particle?
        if self.surname[0] is None:
            particle = ''

        else:
            particle = f"{{{self.surname[0].lower()}}} "

# Main name.
        titles.append(
            particle + self._normalized_name(self.surname[1])
        )

# Just gather all the parts.
        titles = ', '.join(titles)

        return titles

###
# prototype::
#     name : a name to be normalized.
#
#     :return: name in "titlecase" without unnecessary spaces.
###
    def _normalized_name(
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
#     :return: ''None'', or a normalized email adresss.
#
#
# caution::
#     According to RFC 5321, we have:
#         + The domain part is case-insensitive, and should be
#         lowercase.
#         + The local part ***may** be case-sensitive, but rarely
#         is.
###
    def _normalized_email(self) -> str | None:
        email = self.email

# Nothing to do.
        if email is None:
            return email

# Let's normalize the email.
        local_part, _, domain_part = email.partition('@')

        norm_email = f"{local_part}@{domain_part.lower()}"

        return norm_email
###
# prototype::
#     :return: ''None'', or the affiliation adresss without
#              unnecessary spaces.
###
    def _normalized_affiliation(self) -> str | None:
        affiliation = self.affiliation

# Nothing to do.
        if affiliation is None:
            return affiliation

# Let's normalize the affiliation.
        norm_affiliation = single_spaces(affiliation)

        return norm_affiliation

###
# prototype::
#     :return: the number of errors by the validation process
#              of email and membership addresses.
#
#
# important::
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


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print("----------")
    print("GOOD CASES")
    print("----------")

    someone = Person(
        std         = "ALIce,    MarIE   -  LiSe,   {DE}   Charlène  [  support@OpenAI.CoM  ]     (Université   de   la Technologie,    France)",
        firstnames  = ["ALIce", "MarIE  -  LiSe"],
        surname     = ("DE", "Charlène"),
        email       = "support@OpenAI.CoM",
        affiliation = "Université   de   la Technologie,    France"
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
        std         = "A, B, C [  support@openaicom ] (Université de la Techlogie, France)",
        firstnames  = ["A", "B"],
        surname     = "C",
        email       = "support@openaicom",
        affiliation = "Université de la Techlogie, France"
    )

    print()
    print(f"{someone.std}")
    print(f"  + Nb pbs = {someone.validate()}")
