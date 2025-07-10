#!/usr/bin/env python3

import aboutmeta


# ------------- #
# -- IMPORTS -- #
# ------------- #

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

LICENSES_JSON_FILE = Path(__file__).parent / "licenses.json"

TAG_SPDX_LICENSES     = 'licenses'
TAG_SPDX_LICENSE_ID   = 'licenseId'
TAG_SPDX_LICENSE_REF  = 'reference'
TAG_SPDX_LICENSE_NAME = 'name'


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : the \lic code provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''aboutmeta.data.license.License''
#              to work easily with the license.
###
def parser(content: str) -> aboutmeta.data.license.License:
# Our local data.
    with LICENSES_JSON_FILE.open(mode = "r") as f:
        all_licenses = json_load(f)

# Normal form found?
    normal_ID  = normalize(content)

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

    spdx_infos = all_licenses[normal_ID]

# The job has been done.
    return aboutmeta.data.license.License(
        std  = spdx_infos["std"],
        name = spdx_infos["name"],
        ref  = spdx_infos["ref"],
    )


###
# prototype::
#     text : a \lic code.
#
#     :return: a normalized code for the data process.
#
# note::
#     The construction of the path::licenses.json file verifies that
#     normalization does not create any duplicates.
###
def normalize(text: str) -> str:
    text = re.sub(r"[\s_\-\.]+", "", text.lower())

    return text


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
        normal_ID  = normalize(license_ID)

        if normal_ID in licenses:
            raise Exception(
                 "unbijective normal transofrmation of license names:"
                 "\n"
                f"{license_ID} --> {normal_ID}. "
                 "BUG!"
            )

        licenses[normal_ID] = {
            'std' : license_ID,
            'name': lic[TAG_SPDX_LICENSE_NAME],
            'ref' : lic[TAG_SPDX_LICENSE_REF],
        }

    LICENSES_JSON_FILE.write_text(json_dumps(licenses))


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
# Update the license data.
    tool_update_license_json()

# Working examples.
    for lic in [
        "gpl - 3.0 +",
        "cc    by nc 4.0",
    ]:
        print()
        print(f'--- ({lic})')

        liccode = parser(lic)

        print(liccode)
        print(repr(liccode))

    print()

# Corrupted data.
    lic = "gpl"
    lic = "cc nc"
    # lic = "cc"
    # lic = " "

    print(f'--- ({lic}) --> CORRUPTED! Possible matches...')

    liccode = parser(lic)
