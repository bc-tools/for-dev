#!/usr/bin/env python3

from typing import (
    Literal,
    TypeAlias
)


import fnmatch
import re

from pathlib import Path


from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ---------- #
# -- DATA -- #
# ---------- #

TAG_TOC_PATH_RAW = 'raw'

TAG_TOC_GLOB_PATTERNS = [
    TAG_TOC_PATH_GLOB       := 'glob',
    TAG_TOC_PATH_GLOB_RECU  := 'r-glob',
]

TAG_TOC_PATTERN_KINDS = TAG_TOC_GLOB_PATTERNS + [
    TAG_TOC_PATH_REGEX      := 'regex',
    TAG_TOC_PATH_REGEX_RECU := 'r-regex',
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


TYPE_GLOB_KEYS: TypeAlias = Literal[
    TAG_TOC_PATH_GLOB,
    TAG_TOC_PATH_GLOB_RECU
]

TYPE_REGEX_KEYS: TypeAlias = Literal[
    TAG_TOC_PATH_REGEX,
    TAG_TOC_PATH_REGEX_RECU
]

TYPE_TOC_PATH_SPEC: TypeAlias = (
      str
    | dict[TYPE_GLOB_KEYS, str]
    | dict[TYPE_REGEX_KEYS, re.Pattern]
)


###
# prototype::
#     spec   : the specification of a path or search pattern for
#              paths.
#     parent : the parent directory attached to the paths.
#
#
# note::
#     The ''spec'' attribute is standardized to be a dictionary
#     using only one of the following keys.
#
#         * TAG_TOC_PATH_GLOB
#         * TAG_TOC_PATH_GLOB_RECU
#         * TAG_TOC_PATH_RAW
#         * TAG_TOC_PATH_REGEX
#         * TAG_TOC_PATH_REGEX_RECU
###
class TOCPath(DataManager):
    spec  : TYPE_TOC_PATH_SPEC
    parent: Path

###
# prototype::
#     :action: we standardize the ''spec'' attribute and validate the
#              search pattern syntax if needed.
###
    def __post_init__(self) -> None:
        spec = self.spec

# A raw path.
        if isinstance(spec, str):
            self.spec = {TAG_TOC_PATH_RAW: spec}

            return

# A dict spec.
        if len(spec.keys()) != 1:
            raise ParsingError(
                 "Single key dict expected. "
                f"See {spec = }."
            )

# Let's work with a single pattern.
        for kind, pattern in spec.items(): # Python is funny...
            ...

# Legal kind?
        kind = TAG_TOC_PATTERN_ABBREV.get(kind, kind)

        if not kind in TAG_TOC_PATTERN_KINDS:
            raise ParsingError(
                f"Unknow pattern kind ''{kind}''."
            )

# Legal pattern?
        if kind in TAG_TOC_GLOB_PATTERNS:
            self._validate_syntax_glob(pattern)

        else:
            ...




# Syntax is good, but maybe the pattern gives nothing.
        self.spec = {kind: pattern}



###
# prototype::
#     :action: XXX
###
    def _validate_syntax_glob(
        self,
        pattern: str
    ) -> None:
        in_bracket = False
        escaped    = False

        for i, char in enumerate(pattern):
            if escaped:
                escaped = False
                continue

            if char == '\\':
                escaped = True
                continue

            if char == '[':
                in_bracket = True
            elif char == ']':
                if not in_bracket:
                    raise ParsingError(
                        f"Crochet fermant ']' inattendu à l'index {i}."
                    )
                in_bracket = False

        if in_bracket:
            raise ParsingError("Crochet '[' ouvert mais jamais fermé.")

        try:
            regex_str = fnmatch.translate(pattern)
            re.compile(regex_str)

        except (re.error, TypeError):
            raise ParsingError(
                f"Illegal glob pattern ''{pattern}''."
            )


###
# prototype::
#     :action: XXX
#
#     :see: self._validate_parent_dir
###
    def validate(self) -> None:
        self.data_pb.start()

        self._validate_parent_dir()

# Validation regarding the kind of data.
        for kind, pattern in spec.items(): # Python is funny...
            ...

        if kind == TAG_TOC_PATH_RAW:
            ...

        elif kind in TAG_TOC_GLOB_PATTERNS:
            ...

        else:
            ...

###
# prototype::
#     :action: XXX
###
    def _validate_parent_dir(self) -> None:
        self.data_pb.what("parent dir")

# We want an existing parent directory.
        self.data_pb.checking(self.parent)

        if not self.parent.is_dir():
            self.data_pb.new_error(
                data      = self.parent,
                error_msg = "Directory does not exist.",
            )




# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from aboutmeta.core.log_conf import *
    setup_logging()

    THIS_DIR = Path(__file__).parent


# CONSTANTS
    print('')
    print("-- CONSTANTS --")

    print(f'{TAG_TOC_PATTERN_ABBREV = }')


# GOOD
    print()
    print("-- GOOD CASES --")

    for yaml_data in [
# Raw data.
        Path(__file__).name,
# Dict data.
        {'glob': "*.md"},
        {'g': "*\[.md"},
        {'rg': "*.md"},
    ]:
        mydata = TOCPath(
            spec   = yaml_data,
            parent = THIS_DIR
        )

        print()
        print('~~~')

        print()
        print(f"{yaml_data = }")
        print(f"{mydata    = }")

        # print()
        # print(f"Validation process")
        # mydata.validate()

# BAD
    # exit()

    print('')
    print("-- BAD CASES --")

    for yaml_data in [
# Raw data.
        1234,
# Dict data.
        {'g': "*.md", 'r': "*.md"},
        {'gob': "*.md"},
        {'glob': "**/[a-z"},
    ]:
        print()
        print(f"{yaml_data = }")

        try:
            TOCPath(
                spec   = yaml_data,
                parent = THIS_DIR
            )

        except Exception as e:
            print(type(e).__name__, ':', e)

            notes = getattr(e, "__notes__", [])

            for i, n in enumerate(notes, start = 1):
                print(f'[{i}]. {n}')
