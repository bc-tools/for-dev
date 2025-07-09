#!/usr/bin/env python3

import aboutmeta


# ------------- #
# -- IMPORTS -- #
# ------------- #

import                     json
from pathlib        import Path
import                     re

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

### TODO
# prototype::
#     content : XXX
#
#     :return: XXX
###
def parser(content: str) -> aboutmeta.data.license.License:
# Our local data.
    with LICENSES_JSON_FILE.open(mode = "r") as f:
        all_licenses = json.load(f)

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


### TODO
# prototype::
#     text : XXX
#
#     :return: XXX
###
def normalize(text):
    text = re.sub(r"[\s_\-\.]+", "", text.lower())

    return text


### TODO
# prototype::
#     text : XXX
#
#     :return: XXX
###
def license_matches(
    normal_ID,
    max_suggestions = 5,
    min_score       = 60
):
# Our local data.
    with LICENSES_JSON_FILE.open(mode = "r") as f:
        all_licenses = json.load(f)

    all_norm_IDs = list(all_licenses.keys())

# Remove "__version__".
    del all_norm_IDs[0]

# Ask to ''rapidfuzz'' to help us...
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
            fuzzy_matches_filtered.append((orig_key,all_licenses[orig_key]['std']))

    combined = []

    for match in fuzzy_matches_filtered:
        if match[1] not in combined:
            combined.append(match[1])

    return combined[:max_suggestions]


# ----------- #
# -- TOOLS -- #
# ----------- #

from urllib.request import urlopen

### TODO
# prototype::
#     content : XXX
#
#     :return: XXX
###
def tool_update_license_json() -> None:
    SPDX_URL = "https://raw.githubusercontent.com/spdx/license-list-data/main/json/licenses.json"

# The SPDX data online.
    with urlopen(SPDX_URL) as response:
        spdx_data = json.load(response)

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

    LICENSES_JSON_FILE.write_text(json.dumps(licenses))




# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
    tool_update_license_json()

    for lic in [
        "gpl-3.0+",
        "cc    by nc 4.0",
        # "gpl",   # Test of an exception with suggestions.
        # "cc nc",   # Test of an exception with suggestions.
        # "cc",     # Test of an exception without suggestion.
        # " ",     # Test of an exception without suggestion.
    ]:
        liccode = parser(lic)

        print()
        print(f'--- ({lic})')

        print(liccode)
        print(repr(liccode))
