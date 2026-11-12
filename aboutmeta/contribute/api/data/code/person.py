#!/usr/bin/env python3

import httpx

from dataclasses import field

from email_validator import validate_email

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.validate     import validate_type

from aboutmeta.tools.group import (
    extract_group,
    gather_groups,
)

from aboutmeta.tools.spacing import (
    no_space_around,
    single_spaces
)


# ---------- #
# -- DATA -- #
# ---------- #

TAG_AFFI_OPEN    , TAG_AFFI_CLOSE     = '()'
TAG_EMAIL_OPEN   , TAG_EMAIL_CLOSE    = '[]'
TAG_PARTICLE_OPEN, TAG_PARTICLE_CLOSE = '{}'

DELIMS_EMAIL       = TAG_EMAIL_OPEN + TAG_EMAIL_CLOSE
DELIMS_AFFILIATION = TAG_AFFI_OPEN + TAG_AFFI_CLOSE
ALL_DELIMS         = [
    '',
    DELIMS_EMAIL,
    DELIMS_AFFILIATION
]

DELIMS_PARTICLE = TAG_PARTICLE_OPEN + TAG_PARTICLE_CLOSE


###
# prototype::
#     spec        : person \spec.
#     surname     : surname without a particle is mandatory.
#     particle    : surname particle, or ''""'' if no particle is
#                   needed.
#     firstnames  : first name list (that can be an empty list).
#     email       : email adress, or ''""'' if no email provided.
#     affiliation : affiliation adress, or ''""'' if no affiliation
#                   provided.
#
#
# note::
#     The ''surname'', ''particle'', ''firstnames'', ''email''
#     and ''affiliation'' \attrs are build from the value of the
#     ''spec'' \att.
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
#     :action: mandatory validations of ''self.spec'' type, and
#              derivation of the ''surname'', ''particle'',
#              ''firstnames'', ''email'' and ''affiliation''
#              \attrs from ''self.spec''.
###
    def __post_init__(self) -> None:
        validate_type(
            var_name       = 'spec',
            value          = self.spec,
            expected_types = str,
        )

# We can work.
        spec = self.spec.strip()

# One affiliation?
        spec, self.affiliation = extract_group(
        content = spec,
        delims  = DELIMS_AFFILIATION,
        context = 'affiliation'
    )

# One email?
        spec, self.email = extract_group(
            content = spec,
            delims  = DELIMS_EMAIL,
            context = 'email'
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
            context      = 'surname',
            data_on_left = False
        )

# We can update the ''spec'' attribute.
        self._update_spec()

###
# prototype::
#     :action: update the ''spec'' \attr using to the actual \vals
#              of other \attrs.
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
            delims = ALL_DELIMS,
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
#     ''"ALIce,  MarIE   -  LiSe,   {DE}   Charlène"'' becomes
#     ''"Alice, Marie-Lise, {de} Charlène"''.
#
#     + Some valid emails adresses use typographical quirks.
#     For example, ''"SuPpOrT@OpeAI.CoM"'' is valid, but its
#     normalized version, produced by this method, is
#     ''"SuPpOrT@openai.com"''. See the ''_normalize_email''
#     method for technical details.
#
#     + The normalization of the affiliation address is limited
#     to not having consecutive spaces.
#     For example,
#     ''"Université   de   la Technologie,    France"'' becomes
#     ''"Université de la Technologie, France"''.
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
#     name : name to be normalized.
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
#           be lowercase.
#
#         + The local part ***may*** be case-sensitive, but
#           rarely is.
###
    def _normalize_email(self) -> None:
        if self.email:
            local_part, _ , domain_part = self.email.partition('@')

            self.email = f'{local_part}@{domain_part.lower()}'

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
#     :action: the external \func ''email_validator.validate_email''
#              checks the email validity.
###
    def _validate_email(self) -> None:
        self.data_pb.what('email')

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
        self.data_pb.what('affiliation')

# Nothing to do.
        if not self.affiliation:
            self.data_pb.no_check()

            return

# Let's validate the affiliation.
        affi = self.affiliation

        try:
            self.data_pb.checking(affi)

            response = httpx.get(
                'https://nominatim.openstreetmap.org/search',
                params = {
                    'q'     : affi,
                    'format': 'json',
                    'limit' : 1,
                },
                headers = {
                    'User-Agent': 'AdresseChecker/1.0'
                },
                timeout = 3
            )

            if response.is_success and len(response.json()) != 0:
                self.data_pb.validated(affi)

                return

            else:
                self.data_pb.new_error(
                    data      = affi,
                    error_msg = 'Nothing found by OpenStreetMap.',
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

if __name__ == '__main__':
# dev:
    INTERACTIVE_SESSION = True
    INTERACTIVE_SESSION = False
# :dev

    from random import Random

    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

# dev:
    if INTERACTIVE_SESSION:
        from aboutmeta.core.log_conf import *

        setup_logging()

        for yaml_data in [
            # Good cases.
            "Alice, Marie-lise, Someone (My address)",
            "{mc} Someone [support@opeai.com] (My address)",
            # Bad cases.
            "A, B, C [support@openaicom] (Université de la Techlogie, France)",
        ]:
            mydata = Person(spec = yaml_data)

            print("---")
            print(f"{yaml_data = }")
            print(f"{mydata    = }")

            print()
            print("Normalization")
            mydata.normalize()
            print(f"{mydata = }")

            print()
            print("Validation process")
            print(f"{mydata = }")

            mydata.validate()

            for m in mydata._errors_found:
                print(f"    > {m}")
# :dev

# -- Weird spacing -- #
    @given(
        std_spec = st.sampled_from([
            'Alice, Marie-lise, {mc} Someone [e.mail@provided.by]',
        ]),
        rnd = st.randoms(),
    )
    def test_weird_spacing(
        std_spec: str,
        rnd     : Random
    ) -> None:
        weird_spec = ' '.join([
            p + ' '*rnd.randint(0,5)
            for p in std_spec.split(' ')
        ])

        weird_data = Person(spec = weird_spec)

        assert weird_data.spec == std_spec

    test_weird_spacing()

# -- Normalize weird letter casing -- #
    @given(
        std_spec = st.sampled_from([
            '{mc} Someone',
            'Alice, Marie-Lise, {mc} Someone',
            'Alice, Marie-Lise, {mc} Someone [e.mail@provided.by]',
        ]),
        rnd = st.randoms(),
    )
    def test_weird_letter_casing(
        std_spec: str,
        rnd     : Random
    ) -> None:
        def weirdcase(text):
            return ''.join([
            rnd.choice([c.lower(), c.upper()])
            for c in text.strip()
        ])

        if '[' in std_spec:
            before_email, _ , email = std_spec.partition('[')

            email = email[:-1]

            local_part, _ , domain_part = email.partition('@')

            before_email = weirdcase(before_email)
            domain_part  = weirdcase(domain_part)

            weird_spec = f'{before_email} [{local_part}@{domain_part}]'

        else:
            weird_spec = weirdcase(std_spec)

        weird_data = Person(spec = weird_spec)
        weird_data.normalize()

        assert weird_data.spec == std_spec, weird_data.spec

    test_weird_letter_casing()

# -- Illegal spec -- #
    @given(
        yaml_data = st.sampled_from([
            'Someone (My address) [e.mail@provided.by]',
            'Someone [e.mail@provided.by (My address)',
            'Someone [e.mail@provided.by] (My address',
        ]),
    )
    def test_illegal_spec(yaml_data: str) -> None:
        with pytest.raises(ParsingError) as e:
            Person(spec = yaml_data)

# -- Illegal data type -- #
    @given(
        yaml_data = st.sampled_from([
            None,
            123,
        ]),
    )
    def test_illegal_data_type(yaml_data: object) -> None:
        with pytest.raises(TypeError) as e:
            Person(spec = yaml_data)

# dev:
        print('---')
        print(f'{yaml_data = }')
        print(e)
# :dev

    test_illegal_data_type()
