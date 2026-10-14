#!/usr/bin/env python3

import requests

from dataclasses import field

from email_validator import validate_email

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError

from aboutmeta.tools.group import (
    extract_group,
    gather_groups,
)

from aboutmeta.tools.misc  import (
    no_space_around,
    single_spaces
)


# ---------- #
# -- DATA -- #
# ---------- #

TAG_YAML_AFFILIATION_OPEN, TAG_YAML_AFFILIATION_CLOSE = '()'
TAG_YAML_EMAIL_OPEN      , TAG_YAML_EMAIL_CLOSE       = '[]'
TAG_YAML_PARTICLE_OPEN   , TAG_YAML_PARTICLE_CLOSE    = '{}'

DELIMS_EMAIL       = TAG_YAML_EMAIL_OPEN + TAG_YAML_EMAIL_CLOSE
DELIMS_AFFILIATION = TAG_YAML_AFFILIATION_OPEN + TAG_YAML_AFFILIATION_CLOSE
DELIMS_PERSON      = ['',DELIMS_EMAIL, DELIMS_AFFILIATION]

DELIMS_PARTICLE = TAG_YAML_PARTICLE_OPEN + TAG_YAML_PARTICLE_CLOSE

###

# prototype::
#     spec        : the specification of a person.
#     surname     : the surname without a particle is mandatory.
#     particle    : the particle of a surname, or ''""'' if no
#                   particle is needed.
#     firstnames  : the list of first names (that can be an empty
#                   list).
#     email       : the email adress, or ''""'' if no email
#                   provided.
#     affiliation : the affiliation adress, or ''""'' if no
#                   affiliation provided.
#
#
# note::
#     The ''surname'', ''particle'', ''firstnames'', ''email'' and
#     ''affiliation'' attributes are build from the value of the
#     ''spec'' attribute.
###
class Person(DataManager):
    spec       : str
    surname    : str        = field(init = False)
    particle   : str        = field(init = False)
    firstnames : tuple[str] = field(init = False)
    email      : str        = field(init = False)
    affiliation: str        = field(init = False)

###
# prototype::
#     :action: derive the ''surname'', ''particle'', ''firstnames'',
#              ''email'' and ''affiliation'' attributes attributes
#              from ''self.spec''.
###
    def __post_init__(self) -> None:
        spec = self.spec

# One affiliation?
        spec, self.affiliation = extract_group(
        content = spec,
        delims  = DELIMS_AFFILIATION,
        context = "affiliation"
    )

# One email?
        spec, self.email = extract_group(
            content = spec,
            delims  = DELIMS_EMAIL,
            context = "email"
        )

# First names.
        titles = spec.split(',')

        if len(titles) == 1:
            self.firstnames = []

        else:
            self.firstnames = [n.strip() for n in titles[:-1]]

# Surname.
        self.surname, self.particle = extract_group(
            content      = titles[-1].strip(),
            delims       = DELIMS_PARTICLE,
            context      = "surname",
            data_on_left = False
        )

# We can update the ''spec'' attribute.
        self._update_spec()

###
# prototype::
#     :action: update the ''spec'' attribute using to the actual
#              values of other attributes.
###
    def _update_spec(self) -> None:
# Build the standard spec definition.
        self.spec = self.surname

        if not self.particle is None:
            self.spec = f'{{{self.particle}}} {self.spec}'

        if self.firstnames:
            firstnames = ', '.join(self.firstnames)
            self.spec  = f'{firstnames}, {self.spec}'

        self.spec = gather_groups(
            groups = [
                self.spec,
                (
                    ''
                    if self.email is None else
                    self.email
                ),
                (
                    ''
                    if self.affiliation is None else
                    self.affiliation
                ),
            ],
            delims = DELIMS_PERSON,
        )

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
        self._update_spec()

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
        if not self.particle is None:
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
#     :action: email and affiliation validation.
#
#     :see: self._validate_email,
#           self._validate_affiliation
###
    def validate(self) -> None:
        self.data_pb.start()

        self._validate_email()
        self._validate_affiliation()

###
# prototype::
#     :action: ''email_validator.validate_email'' checks
#              the email validity.
###
    def _validate_email(self) -> None:
        self.data_pb.what("email")

# Nothing to do.
        if not self.email:
            self.data_pb.no_check()

            return

# Let's validate the email.
        email = self.email

        try:
            self.data_pb.checking(email)
            validate_email(email)
            self.data_pb.validated(email)

        except Exception as e:
            self.data_pb.new_exception(
                data       = email,
                _exception = e,
            )

            self.data_pb.rejected(email)

###
# prototype::
#     :action: OpenStreetMap is used to verify the existence
#              of the affiliation.
###
    def _validate_affiliation(self) -> None:
        self.data_pb.what("affiliation")

# Nothing to do.
        if not self.affiliation:
            self.data_pb.no_check()

            return

# Let's validate the affiliation.
        affi = self.affiliation

        try:
            self.data_pb.checking(affi)

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

            if response.ok and len(response.json()) != 0:
                self.data_pb.validated(affi)

                return

            else:
                self.data_pb.new_error(
                    data      = affi,
                    error_msg = "Nothing found by OpenStreetMap.",
                )

        except Exception as e:
            self.data_pb.new_exception(
                data       = affi,
                _exception = e,
            )

        self.data_pb.rejected(affi)


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from aboutmeta.core.log_conf import *
    setup_logging()


# GOOD
    print()
    print("-- GOOD CASES --")

    for spec in [
        "Someone",
        "ALIce, MarIE-LiSe,  Someone    (My address)",
        "{Mc} Someone    [e.mail@provided.by]",
        "Someone [e.mail@provided.by] (My address)",
        "ALIce,    MarIE-LiSe,   {MC}    Someone     [   e.mail@provided.by ]    (   My   address  )",
    ]:
        mydata = Person(spec = spec)

        print()
        print('~~~')

        print()
        print(f"{spec   = }")
        print(f"{mydata = }")

        print()
        print("Normalization")
        mydata.normalize()
        print(mydata)

        print()
        print(f"Validation process")
        mydata.validate()

# BAD
    # exit()

    print()
    print("-- BAD VALIDATION CASES --")

    for spec in [
        "A, B, C [support@openaicom] (Université de la Techlogie, France)",
    ]:
        print()
        print(f"{spec = }")

        mydata = Person(spec = spec)
        mydata.validate()

        for m in mydata._errors_found:
            print(f"    > {m}")


    # exit()

    print()
    print("-- BAD PARSING CASES --")

    for spec in [
        "Someone (My address) [e.mail@provided.by]",
        "Someone [e.mail@provided.by (My address)",
        "Someone [e.mail@provided.by] (My address",
    ]:
        print()
        print(f"{spec = }")

        try:
            Person(spec = spec)

        except Exception as e:
            print(type(e).__name__, ':', e)
