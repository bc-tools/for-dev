#!/usr/bin/env python3


# --------- #
# -- TOC -- #
# --------- #

TAG_TOC_GLOB_PATTERNS = [
    TAG_TOC_PATH_GLOB       := "glob",
    TAG_TOC_PATH_RECU_GLOB  := "r-glob",
]

TAG_TOC_PATTERN_KINDS = TAG_TOC_GLOB_PATTERNS + [
    TAG_TOC_PATH_REGEX      := "regex",
    TAG_TOC_PATH_RECU_REGEX := "r-regex",
]

TAG_TOC_PATTERN_ABBREV = {}

for t in TAG_TOC_PATTERN_KINDS:
    if '-' in t:
        a = t[:3]
        a = a.replace('-', '')

    else:
        a = t[0]

    TAG_TOC_PATTERN_ABBREV[a] = t


# ---------------- #
# -- DELIMITERS -- #
# ---------------- #

TAG_YAML_AFFILIATION_OPEN, TAG_YAML_AFFILIATION_CLOSE = "()"
TAG_YAML_EMAIL_OPEN      , TAG_YAML_EMAIL_CLOSE       = "[]"
TAG_YAML_PARTICLE_OPEN   , TAG_YAML_PARTICLE_CLOSE    = "{}"

DELIMS_EMAIL       = TAG_YAML_EMAIL_OPEN + TAG_YAML_EMAIL_CLOSE
DELIMS_AFFILIATION = TAG_YAML_AFFILIATION_OPEN + TAG_YAML_AFFILIATION_CLOSE
DELIMS_PERSON      = ["",DELIMS_EMAIL, DELIMS_AFFILIATION]

DELIMS_PARTICLE = TAG_YAML_PARTICLE_OPEN + TAG_YAML_PARTICLE_CLOSE
