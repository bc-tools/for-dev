#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.data import (
    constants,
    license
)

from typing import List

from json import (
    dumps as json_dumps,
    load  as json_load,
)

from pathlib import Path
import              re

from rapidfuzz import (
    process as fuzz_process,
    fuzz
)


# --------------- #
# -- CONSTANTS -- #
# --------------- #

LICENSES_JSON_FILE = Path(__file__).parent / "default-licenses.json"


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : the \lic code provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''license.License'' to work
#              easily with the license.
###
def parser(content: str) -> license.License:
# Our local data.
    with LICENSES_JSON_FILE.open(mode = "r") as f:
        all_licenses = json_load(f)

# Normal form found?
    normal_ID  = _normalize_lic_code(content)

    if normal_ID not in all_licenses:
        extra       = ''
        suggestions = license_matches(normal_ID)

        if suggestions:
            plurial = '' if len(suggestions) == 1 else 'es'
            extra   = f"\nPossible match{plurial} found.\n" + '\n'.join(
                f"  * {s}" for s in suggestions
            )

        else:
            extra = " No match found."

        raise ValueError(
            f"unknown license code ''{content}''.{extra}"
        )

# Deprecated?
    if all_licenses[normal_ID]["deprecated"]:
        raise ValueError(
            f"deprecated license code ''{all_licenses[normal_ID]['std']}''."
        )

# Living license found.
    spdx_infos = all_licenses[normal_ID]

# The job has been done.
    return license.License(
        std        = spdx_infos["std"],
        name       = spdx_infos["name"],
        ref        = spdx_infos["ref"],
        deprecated = spdx_infos["deprecated"],
    )


###
# prototype::
#     code : a \lic code.
#
#     :return: a normalized code for the data process.
#
# note::
#     The construction of the path::licenses.json file verifies that
#     normalization does not create any duplicates.
###
def _normalize_lic_code(code: str) -> str:
    code = re.sub(
        r"[\s_\-\.]+",
        "",
        code.lower()
    )

    return code


###
# prototype::
#     normal_ID       : an invalid normalized \lic code.
#     max_suggestions : the maximum \nb of suggestions proposed.
#
#     :return: possible matches for a valid SPDX \lic code.
###
def license_matches(
    normal_ID      : str,
    max_suggestions: int = 15
) -> List[str]:
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
#     :action: build a local \std version of the online SPDX
#              path::''licenses.json'' file.
###
def tool_update_license_json() -> None:
    import requests

    SPDX_URL = "https://raw.githubusercontent.com/spdx/license-list-data/main/json/licenses.json"

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
                 "unbijective normal transofrmation of license names:"
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


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
# Update the license data.
    tool_update_license_json()

# Working examples.
    for lic_ID in [
        "gpl - 3.0 only ",
        "cc    by nc 4.0",
    ]:
        print()
        print(f'--- ({lic_ID})')

        lic_data = parser(lic_ID)

        print(lic_data)
        print(repr(lic_data))

    print()

# Corrupted data.
    lic_ID = "gpl  3.0 +"

    # lic_ID = "gpl"
    # lic_ID = "cc nc"
    # lic_ID = "cc"
    # lic_ID = " "

    print(f'--- ({lic_ID}) --> CORRUPTED! Possible matches...')

    lic_data = parser(lic_ID)
