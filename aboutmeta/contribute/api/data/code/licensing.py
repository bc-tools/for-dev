#!/usr/bin/env python3

from json import load as json_load

from pathlib import Path
import              re

from rapidfuzz import (
    process as fuzz_process,
    fuzz
)


from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError
from aboutmeta.core.validate     import validate_type


# ---------- #
# -- DATA -- #
# ---------- #

LICENSES_JSON_FILE = (
    Path(__file__).parent / f"{Path(__file__).stem}-spdx.json"
)


_PATTERN_NORMALIZED_LICENSE_CODE = re.compile(r"[\s_\-\.]+")


###
# prototype::
#     spdx_id : short \spdx identifier, such as ''"GPL-3.0-only"'',
#               but flexible writings allowed like ''"gpl 3.0 only"'.
#     name    : the full license name like ''"GNU General Public
#               License v3.0 only"''.
#     url     : the \url linking to the \spdx online description of
#               the license.
#
#
# note::
#     The ''name'' and ''url'' \attrs are build from the value of
#     the ''spdx_id'' \attr.
#
#
# warning::
#     Identifiers are automatically normalized regardless of letter
#     casing: ''"gpl 3.0 only"'' is saved as ''"GPL-3.0-only"''.
###
class Licensing(DataManager):
    spdx_id: str
    name   : str = field(init = False)
    url    : str = field(init = False)

###
# prototype::
#     :action: mandatory validations of ''self.spec'' type, and
#              derivation of the ''name'' and ''url'' \attrs from
#              ''self.spdx_id'' and expand the identifier to its
#              normalized form (e.g., ''"gpl 3.0 only"'' becomes
#              ''"GPL-3.0-only"'').
###
    def __post_init__(self) -> None:
        validate_type(
            data_name      = 'spdx_id',
            data           = self.spdx_id,
            types_expected = str,
        )

# Our local data.
        with LICENSES_JSON_FILE.open(mode = "r") as f:
            all_licenses = json_load(f)

# We need a normal form.
        normal_ID  = _normalize_lic_code(self.spdx_id)

        if normal_ID not in all_licenses:
            extra       = ''
            suggestions = _license_matches(normal_ID)

            if suggestions:
                plurial = '' if len(suggestions) == 1 else 'es'
                extra   = f"Possible match{plurial} found.\n"
                extra  += '\n'.join(f"  * {s}" for s in suggestions)

            else:
                extra = "No match found."

            e = ValueError(
                f"unknown license code ''{self.spdx_id}''."
            )

            e.add_note(extra)

            raise e

# Deprecated?
        if all_licenses[normal_ID]["deprecated"]:
            raise ValueError(
                 "deprecated license code "
                f"''{all_licenses[normal_ID]['std']}''."
            )

# Living license found.
        spdx_infos = all_licenses[normal_ID]

# The job has been done.
        self.spdx_id = spdx_infos["std"]
        self.name    = spdx_infos["name"]
        self.url     = spdx_infos["ref"]


###
# prototype::
#     code : a \lic code.
#
#     :return: a normalized code for the data process.
#
#
# note::
#     The construction of the path::''licenses.json'' file verifies
#     that normalization does not create any duplicates.
###
def _normalize_lic_code(code: str) -> str:
    code = _PATTERN_NORMALIZED_LICENSE_CODE.sub("", code.lower())

    return code


###
# prototype::
#     normal_ID       : an invalid normalized \lic code.
#     max_suggestions : the maximum \nb of suggestions proposed.
#
#     :return: possible matches for a valid \spdx \lic code.
###
def _license_matches(
    normal_ID      : str,
    max_suggestions: int = 15
) -> list[str]:
# Our local data.
    with LICENSES_JSON_FILE.open(mode = "r") as f:
        all_licenses = json_load(f)

    all_norm_IDs = list(all_licenses.keys())

# Remove "__version__".
    del all_norm_IDs[0]

# Ask to ''rapidfuzz'' to help us...
    min_score = 60

    fuzzy_matches_raw = fuzz_process.extract(
        normal_ID,
        all_norm_IDs,
        scorer = fuzz.ratio,
        limit  = max_suggestions * 2
    )

    fuzzy_matches_filtered = []

    for norm_match, score, idx in fuzzy_matches_raw:
        if score >= min_score:
            orig_key = all_norm_IDs[idx]

            fuzzy_matches_filtered.append((
                orig_key,
                all_licenses[orig_key]['std']
            ))

    combined = []

    for match in fuzzy_matches_filtered:
        if match[1] not in combined:
            combined.append(match[1])

    return sorted(combined[:max_suggestions])


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# prototype::
#     :action: build a local \std version of the online \spdx
#              path::''licenses.json'' file.
###
def tool_update_license_json() -> None:
    from json import dumps as json_dumps

    import requests

    SPDX_URL  = "https://raw.githubusercontent.com/spdx/"
    SPDX_URL += "license-list-data/refs/heads/main/json/licenses.json"

    TAG_SPDX_LICENSES = 'licenses'

    TAG_SPDX_LICENSE_ID         = 'licenseId'
    TAG_SPDX_LICENSE_NAME       = 'name'
    TAG_SPDX_LICENSE_REF        = 'reference'
    TAG_SPDX_LICENSE_DEPRECATED = "isDeprecatedLicenseId"

# The SPDX data online.
    try:
        response = requests.get(
            url     = SPDX_URL,
            timeout = 5
        )

        if response.status_code == 200:
            spdx_data = response.json()

        elif response.status_code == 404:
            raise FileNotFoundError(
                f"aboutmeta BUG!\nBad SPDX_URL:\n{SPDX_URL}"
            )

        else:
            raise RuntimeError(
                f"HTTP error {response.status_code}."
            )

    except requests.exceptions.RequestException as e:
        raise e

# Our local data.
    licenses = {
        '__version__': spdx_data["licenseListVersion"]
    }

    for lic in spdx_data[TAG_SPDX_LICENSES]:
        license_ID = lic[TAG_SPDX_LICENSE_ID]
        normal_ID  = _normalize_lic_code(license_ID)

        if normal_ID in licenses:
            raise Exception(
                 "unbijective normal transformation of license names:"
                 "\n"
                f"{license_ID} --> {normal_ID}. "
                 "BUG!"
            )

        licenses[normal_ID] = {
            'std'       : license_ID,
            'name'      : lic[TAG_SPDX_LICENSE_NAME],
            'ref'       : lic[TAG_SPDX_LICENSE_REF],
            'deprecated': lic[TAG_SPDX_LICENSE_DEPRECATED]
        }

    LICENSES_JSON_FILE.write_text(json_dumps(licenses))


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# dev:
    UPDATE_LICENSE_MEDATA = True
    UPDATE_LICENSE_MEDATA = False
# :dev


    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

    from aboutmeta.core.errors import YAMLTypeError


# dev:
    if UPDATE_LICENSE_MEDATA:
        tool_update_license_json()

    yaml_data = 'gpl 3.0 only'
    mydata    = Licensing(spdx_id = yaml_data)

    print('---')
    print(f"{yaml_data = }")
    print(f"{mydata    = }")
# :dev


# -- Legal weird license code -- #
    @given(
        full_data = st.sampled_from([
            (
                "gpl   3.0 only ",
                "GPL-3.0-only"
            ),
            (
                "cc -    by    nc- 4.0",
                "CC-BY-NC-4.0"
            ),
        ]),
    )
    def test_legal_weird_license_code(full_data):
        yaml_data, spdx_id = full_data

        mydata = Licensing(spdx_id = yaml_data)

        assert mydata.spdx_id == spdx_id

    test_legal_weird_license_code()


# -- Illegal YAML data type -- #
    @given(
        yaml_data = st.sampled_from([
            None,
            123,
        ]),
    )
    def test_illegal_yaml_data_type(yaml_data):
        with pytest.raises(YAMLTypeError) as e:
            Licensing(spdx_id = yaml_data)

# dev:
        print('---')
        print(f"{yaml_data = }")
        print(e)
# :dev

    test_illegal_yaml_data_type()


# -- Illegal license code -- #
    @given(
        yaml_data = st.sampled_from([
            "gpl  3.0 +",
            "gpl",
            "cc nc",
            "cc",
            "",
        ]),
    )
    def test_illegal_license_code(yaml_data):
        with pytest.raises(ValueError) as e:
            Licensing(spdx_id = yaml_data)

# dev:
        print('---')
        print(f"{yaml_data = }")
        print(e)
# :dev

    test_illegal_license_code()
