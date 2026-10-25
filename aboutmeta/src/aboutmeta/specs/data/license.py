#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/data/code/license.py'


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


# ---------- #
# -- DATA -- #
# ---------- #

LICENSES_JSON_FILE = Path(__file__).parent / "license-spdx.json"


_PATTERN_NORMALIZED_LICENSE_CODE = re.compile(r"[\s_\-\.]+")


###
# prototype::
#     spdx_id : short SPDX identifier, such as ''GPL-3.0-only'',
#               but flexible writings allowed like ''gpl 3.0 only'.
#     name    : the full license name like ''GNU General Public
#               License v3.0 only''.
#     url     : the URL linking to the SPDX online description of
#               the license.
#
#
# note::
#     The ''name'' and ''url'' attributes are build from the value
#     of the ''spdx_id'' attribute.
#
#
# warning::
#     Identifiers are automatically normalized regardless of letter
#     casing: if a user enters ''gpl 3.0 only'' it will be saved as
#     ''GPL-3.0-only''.
###
class License(DataManager):
    spdx_id: str
    name   : str = field(init = False)
    url    : str = field(init = False)

###
# prototype::
#     :action: derive the ''name'' and ''url'' attributes from
#              ''self.spdx_id'' and expand the identifier to its
#              normalized form (e.g., ''gpl 3.0 only'' becomes
#              ''GPL-3.0-only'').
###
    def __post_init__(self) -> None:
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

            e = ParsingError(
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
#     The construction of the path::''licenses.json'' file verifies that
#     normalization does not create any duplicates.
###
def _normalize_lic_code(code: str) -> str:
    code = _PATTERN_NORMALIZED_LICENSE_CODE.sub("", code.lower())

    return code


###
# prototype::
#     normal_ID       : an invalid normalized \lic code.
#     max_suggestions : the maximum \nb of suggestions proposed.
#
#     :return: possible matches for a valid SPDX \lic code.
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
