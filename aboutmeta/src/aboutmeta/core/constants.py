#!/usr/bin/env python3


# --------- #
# -- TOC -- #
# --------- #

TAG_TOC_GLOB_PATTERNS = [
    TAG_TOC_PATH_GLOB       := 'glob',
    TAG_TOC_PATH_RECU_GLOB  := 'r-glob',
]

TAG_TOC_PATTERN_KINDS = TAG_TOC_GLOB_PATTERNS + [
    TAG_TOC_PATH_REGEX      := 'regex',
    TAG_TOC_PATH_RECU_REGEX := 'r-regex',
]

TAG_TOC_PATTERN_ABBREV = {}

for t in TAG_TOC_PATTERN_KINDS:
    if '-' in t:
        a = t[:3]
        a = a.replace('-', '')

    else:
        a = t[0]

    assert not a in TAG_TOC_PATTERN_ABBREV

    TAG_TOC_PATTERN_ABBREV[a] = t


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == '__main__':
    from pprint import pprint

    print('\n------------\n')

    print('TAG_TOC_PATTERN_ABBREV:')
    pprint(TAG_TOC_PATTERN_ABBREV)
