#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/data/code/licensing.py'


from pathlib import Path
import              re

from json import load as json_load

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

LICENSING_JSON_FILE = (
    Path(__file__).parent / f'{Path(__file__).stem}-spdx.json'
)


_PATTERN_REMOVE_SPACES = re.compile(r'[\s_]+')

_SPECIAL_SEPS                = '.-'
_PATTERN_REMOVE_SPECIAL_SEPS = re.compile(r'[\.-]+')


_TAG_DEPRECATED = 'deprecated'
_TAG_STD        = 'std'
_TAG_NAME       = 'name'
_TAG_REF        = 'ref'


###
# prototype::
#     spdx_id : short \spdx identifier, such as ''"GPL-3.0-only"'',
#               but flexible writings allowed like ''"gpl 3.0 only"'.
#     name    : full license name like ''"GNU General Public License
#               v3.0 only"''.
#     url     : \url linking to the \spdx online license description.
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
            expected_types = str,
        )

# Our local data.
        with LICENSING_JSON_FILE.open(mode = 'r') as f:
            all_licenses = json_load(f)

# We need a normal form.
        normal_ID  = _normalize_lic_code(self.spdx_id)

        if normal_ID not in all_licenses:
            extra       = ''
            suggestions = _license_matches(normal_ID)

            if suggestions:
                plurial = '' if len(suggestions) == 1 else 'es'
                extra   = f'Possible match{plurial} found.\n'
                extra  += '\n'.join(f'  * {s}' for s in suggestions)

            else:
                extra = 'No match found.'

            e = ValueError(
                f'unknown license code {self.spdx_id!r}.'
            )

            e.add_note(extra)

            raise e

# Deprecated?
        if all_licenses[normal_ID][_TAG_DEPRECATED]:
            raise ValueError(
                 'deprecated license code '
                f'{all_licenses[normal_ID]['std']!r}.'
            )

# Living license found.
        spdx_infos = all_licenses[normal_ID]

# The job has been done.
        self.spdx_id = spdx_infos[_TAG_STD]
        self.name    = spdx_infos[_TAG_NAME]
        self.url     = spdx_infos[_TAG_REF]


###
# prototype::
#     code : \lic code.
#
#     :return: normalized code for data process.
#
#
# note::
#     The construction of the path::''licenses.json'' file verifies
#     that normalization does not create any duplicates.
###
def _normalize_lic_code(code: str) -> str:
    _code = code.strip()

    if not _code:
        raise ValueError(f'empty license code {code!r}.')

    _code = _PATTERN_REMOVE_SPACES.sub('', _code.lower())

    for s in _SPECIAL_SEPS:
        if s*2 in _code:
            raise ValueError(
                f'illegal license code {code!r} contains {s*2!r} '
                 '(after removing spaces)'
            )

        if _code[-1] == s:
            raise ValueError(
                f'illegal license code {code!r} ends with {s!r} '
                 '(after removing spaces)'
            )

    _code = _PATTERN_REMOVE_SPECIAL_SEPS.sub('', _code)

    return _code


###
# prototype::
#     normal_ID       : invalid normalized \lic code.
#     max_suggestions : maximum \nb of suggestions proposed.
#
#     :return: possible matches for a valid \spdx \lic code.
###
def _license_matches(
    normal_ID      : str,
    max_suggestions: int = 15
) -> list[str]:
# Our local data.
    with LICENSING_JSON_FILE.open(mode = 'r') as f:
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
