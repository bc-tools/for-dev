#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/data/code/toc_path.py'


from typing import Literal

from collections.abc import (
    Callable,
    Iterator,
)


import fnmatch
import re

from pathlib import Path


from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError
from aboutmeta.core.validate     import validate_type


# ---------- #
# -- DATA -- #
# ---------- #

TAG_GLOB_METHOD      = 'glob'
TAG_GLOB_RECU_METHOD = 'rglob'

TAG_TOC_PATH_RAW = 'raw'

TAG_TOC_GLOB_PATTERNS = [
    TAG_TOC_PATH_GLOB      := 'glob',
    TAG_TOC_PATH_GLOB_RECU := 'r-glob',
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


GLOB_KEYS_TYPE = Literal[
    TAG_TOC_PATH_GLOB,
    TAG_TOC_PATH_GLOB_RECU
]

REGEX_KEYS_TYPE = Literal[
    TAG_TOC_PATH_REGEX,
    TAG_TOC_PATH_REGEX_RECU
]

TOC_PATH_SPEC_TYPE = (
      str
    | dict[GLOB_KEYS_TYPE, str]
    | dict[REGEX_KEYS_TYPE, re.Pattern]
)


###
# prototype::
#     spec    : the specification of a relative path or a relative
#               search pattern for paths.
#     parent  : the parent directory for the relative paths.
#     kind    : the kind of path to manage (either a raw path or
#               a pattern).
#             @ _ in TAG_TOC_PATTERN_KINDS
#               or
#               _ = TAG_TOC_PATH_RAW
#     pattern : a pattern or a raw path specified relatively to
#               the ''parent'' directory.
#
#
# note::
#     The ''kind'' and ''pattern'' attributes are build from the
#     value of the ''spec'' attribute.
#
#
# important::
#     A dictionary ''spec'' attribute is standardized: only
#     long-name keys are used, and string ''regex'' patterns are
#     transformed into their compiled versions.
###
class TOCPath(DataManager):
    spec   : TOC_PATH_SPEC_TYPE
    parent : Path
    kind   : str              = field(init = False)
    pattern: str | re.Pattern = field(init = False)

###
# prototype::
#     :action: we standardize the ''spec'' attribute and validate
#              the search pattern syntax if needed.
###
    def __post_init__(self) -> None:
        validate_type(
            data_name      = 'spec',
            data           = self.spec,
            types_expected = (str, dict),
        )

        validate_type(
            data_name      = 'parent',
            data           = self.parent,
            types_expected = Path,
        )

# We can work.
        spec = self.spec

# A raw path.
        if isinstance(spec, str):
            self.kind    = TAG_TOC_PATH_RAW
            self.pattern = spec

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
            self._check_syntax_glob(pattern)

            compiled_pattern = pattern

        else:
            compiled_pattern = self._check_syntax_regex(pattern)

# Syntax is good, but maybe the pattern gives nothing...
        self.kind    = kind
        self.pattern = compiled_pattern
        self.spec    = {kind: pattern}

###
# prototype::
#     pattern : a glob pattern search.
#
#     :action: check well-balanced hooks, and syntax by trying to
#              transform the pattern into a ''regex''.
###
    def _check_syntax_glob(
        self,
        pattern: str
    ) -> None:
# Checking for well-balanced hooks.
        in_bracket = False
        escaping   = False

        for char in pattern:
            if escaping:
                escaping = False

            elif char == '\\':
                escaping = True

            elif char == '[':
                in_bracket = True

            elif char == ']':
                if not in_bracket:
                    raise ParsingError(
                        "Extra closing hook '']''."
                    )

                in_bracket = False

        if in_bracket:
            raise ParsingError("Opening hook ''['' unclosed.")

# Checking pattern validity by trying to transform it into a
# ''regex'' pattern.
        try:
            self._check_syntax_regex(
                fnmatch.translate(pattern)
            )

        except ParsingError as _error:
            e = ParsingError(
                f"Illegal glob pattern ''{pattern}''."
            )

            e.add_note(str(_error))

            notes = getattr(e, "__notes__", [])

            for i, n in enumerate(notes, start = 2):
                e.add_note(n)

            raise e

###
# prototype::
#     pattern : a string ''regex'' pattern search.
#
#     :action: check syntax by compiling the pattern.
#
#     :return: the compile ''regex'' version of the pattern.
###
    def _check_syntax_regex(
        self,
        pattern: str
    ) -> re.Pattern:
        try:
            pattern = re.compile(pattern)

        except (re.error, TypeError) as _error:
            e = ParsingError(
                f"Illegal regex pattern ''{pattern}''."
            )

            e.add_note(str(_error))

            raise e

        return pattern

###
# prototype::
#     :action: check for parent folder existence, unbroken single
#              raw path if needed, or winning pattern validation
#              if needed.
#
#     :see: self._validate_parent_dir,
#           self._validate_raw_path,
#           self._validate_glob_pattern,
#           self._validate_regex_pattern
###
    def validate(self) -> None:
        self.data_pb.start()

        self._validate_parent_dir()

# Validation regarding the kind of data.
        if self.kind == TAG_TOC_PATH_RAW:
            self._validate_raw_path()

        elif self.kind in TAG_TOC_GLOB_PATTERNS:
            self._validate_glob_pattern()

        else:
            self._validate_regex_pattern()

###
# prototype::
#     :action: check for parent folder existence.
###
    def _validate_parent_dir(self) -> None:
        self.data_pb.what("parent dir")
        self.data_pb.checking(self.parent)

        if not self.parent.is_dir():
            self.data_pb.new_error(
                data      = self.parent,
                error_msg = "Directory does not exist.",
            )

        self.data_pb.validated(self.parent)

###
# prototype::
#     :action: check for unbroken raw path.
###
    def _validate_raw_path(self) -> None:
        raw_path = self.pattern

        self.data_pb.what("raw path")
        self.data_pb.checking(raw_path)

        full_path = self.parent / raw_path

        if (
            full_path.is_file()
            or
            full_path.is_dir()
        ):
            self.data_pb.validated(raw_path)

        else:
            self.data_pb.new_error(
                data      = full_path,
                error_msg = f"Inexisting full path. See raw path '{raw_path}'.",
            )

            self.data_pb.rejected(raw_path)

###
# prototype::
#     :action: check for winning ''glob'' pattern.
#
#     :see: self._validate_pattern
###
    def _validate_glob_pattern(self) -> None:
        self._validate_pattern(
            str_pattern = self.pattern,
            path_iter   = self.glob_iter,
        )

###
# prototype::
#     :action: check for winning ''regex'' pattern.
#
#     :see: self._validate_pattern
###
    def _validate_regex_pattern(self) -> None:
        self._validate_pattern(
            str_pattern = self.pattern.pattern,
            path_iter   = self.regex_iter,
        )

###
# prototype::
#     str_pattern : string version of a glob or ''regex'' pattern
#                   (this is for terminal and log communication).
#     path_iter   : an iterartor expected either ''glob'' or
#                   ''rglob'' method name to iterate over paths in
#                   a specific ways.
#
#     :action: check for winning pattern using a specific path
#              iterator.
#
#     :see: self.glob_iter ,
#           self.regex_iter
###
    def _validate_pattern(
        self,
        str_pattern: str,
        path_iter  : Callable[[str], Iterator[Path]],
    ) -> None:
        glob_method_name = self._start_pattern_validation(
            str_pattern = str_pattern
        )

        nothing_found = True

        for p in path_iter(glob_method_name):
            nothing_found = False

            break

        self._close_pattern_validation(
            nothing_found = nothing_found,
            str_pattern   = str_pattern
        )

###
# prototype::
#     str_pattern : :see: self._validate_pattern
#
#     :action: initialization of the pattern validation process.
#
#     :return: the ''glob'' method name to use regarding the
#              ''Path'' class.
#            @ _ = TAG_GLOB_METHOD
#              or
#              _ = TAG_GLOB_RECU_METHOD
#
#     :see: self._is_recu_search
###
    def _start_pattern_validation(
        self,
        str_pattern: str
    ) -> str:
        is_recu = self._is_recu_search()

        if is_recu:
            _ , kind = self.kind.split('-')

        else:
            kind = self.kind

        what = (
            f"recursive {kind}"
            if is_recu else
            kind
        )

        self.data_pb.what(f"{what} pattern")
        self.data_pb.checking(str_pattern)

        glob_method_name = (
            TAG_GLOB_METHOD
            if is_recu else
            TAG_GLOB_RECU_METHOD
        )

        return glob_method_name

###
# prototype::
#     :return: ''True'' for a recursive search, and ''False''
#              otherwise.
###
    def _is_recu_search(self) -> str:
        return (self.kind[:2] == 'r-')

###
# prototype::
#     nothing_found : a ''True'' value indicates that a pattern
#                     gives at least one match, whereas ''False''
#                     indicates a losing pattern.
#     str_pattern   : :see: self._start_pattern_validation
#
#     :action: closing of the pattern validation process.
###
    def _close_pattern_validation(
        self,
        nothing_found: bool,
        str_pattern  : str
    ) -> None:
        if nothing_found:
            self.data_pb.new_error(
                data      = str_pattern,
                error_msg = f"No matches found.",
            )

            self.data_pb.rejected(str_pattern)

        else:
            self.data_pb.validated(str_pattern)

###
# prototype::
#     glob_method_name : :see: self._start_pattern_validation
#                              [return]
#
#     :yield: each path which validates the ''glob'' pattern
#             stored in ''self.pattern'' using the ''glob''
#             method named ''glob_method_name'' from the ''Path''
#             class.
###
    def glob_iter(
        self,
        glob_method_name: str,
    ) -> Iterator[Path]:
        for p in getattr(self.parent, glob_method_name)(
            self.pattern
        ):
            yield p

###
# prototype::
#     glob_method_name : :see: self._start_pattern_validation
#                              [return]
#
#     :yield: each path which validates the ''regex'' pattern
#             stored in ''self.pattern'' using the ''glob''
#             method named ''glob_method_name'' from the ''Path''
#             class.
###
    def regex_iter(
        self,
        glob_method_name: str,
    ) -> Iterator[Path]:
        for p in getattr(self.parent, glob_method_name)('*'):
            relpath = p.relative_to(self.parent)

            if self.pattern.fullmatch(str(relpath)):
                yield p
