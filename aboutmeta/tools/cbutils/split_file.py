#!/usr/bin/env python3

from pathlib import Path
import              re

from .messages import *


# ------------ #
# -- TYPING -- #
# ------------ #

type NestedDictPath = dict[str, Path | NestedDictPath]


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAG_ROOT_HEADER = ".:-R-O-O-T-:."


# -------------------- #
# -- SPLIT IN PARTS -- #
# -------------------- #

###
# prototype::
#     file        : a file to analyze.
#     pat_headers : the list of regular expressions identifying
#                   the headers used to section the content.
#     strip_parts : set to ''True'', the contents are stripped.
#
#     :return: a \dict reflecting the structure of the extracted
#              content according to the relevant header level.
#
#
# note::
#     At the beginning of each piece of content that has not yet
#     been analysed, the basic header is ''TAG_ROOT_HEADER''.
###
def hd_split_file(
    file       : Path,
    pat_headers: list[re.Pattern],
    strip_parts: bool = True,
) -> NestedDictPath:
    return _recu_hd_split_file(
        content     = file.read_text(),
        pat_headers = pat_headers,
        strip_parts = strip_parts,
    )


###
# prototype::
#     content     : a content to analyze.
#     pat_headers : :see: hd_split_file
#     strip_parts : :see: hd_split_file
#
#     :return: :see: hd_split_file
###
def _recu_hd_split_file(
    content    : str,
    pat_headers: list[re.Pattern],
    strip_parts: bool,
) -> NestedDictPath:
# No pattern.
    if not pat_headers:
        return content

# Use of the first pattern.
    parts = dict()
    curhd = TAG_ROOT_HEADER # Current header.

    pattern, *other_patterns = pat_headers

    for i, piece in enumerate(pattern.split(content)):
        if i % 2 == 1:
            curhd = piece.strip()

        else:
            if strip_parts:
                piece = piece.strip()

            parts[curhd] = _recu_hd_split_file(
                content     = piece,
                pat_headers = other_patterns,
                strip_parts = strip_parts,
            )

# Nothing left to do.
    return parts


###
# prototype::
#     mandatory : set of mandatory section titles
#     optional  : set of optional section titles
#     ignored   : set of ignored section titles
#     parts     : parts of the code
#     context   : the context of use
#
#     :action: validation process of the good use of sections
#
#     :see: _raise_unwanted_sections
###
def hd_split_validate(
    mandatory: set[str],
    optional : set[str],
    ignored  : set[str],
    parts    : NestedDictPath,
    context  : str,
) -> None:
    sections_found = set(parts) - set([TAG_ROOT_HEADER])

# No extra sections used?
    all_sections = mandatory | optional | ignored

    if not sections_found <= all_sections:
        _raise_unwanted_sections(
            xtra_sections = sections_found - all_sections,
            what          = 'extra',
            context       = context,
        )

# All mandatory sections used?
    if not mandatory <= sections_found:
        _raise_unwanted_sections(
            xtra_sections = mandatory - sections_found,
            what          = 'missing mandatory',
            context       = context,
        )


###
# prototype::
#     xtra_sections : the extra section list
#     what          : the magic comment kind
#     context       : the context in which an error is raised and
#                     logged.
#
#     :action: log an error and raise an exception.
###
def _raise_unwanted_sections(
    xtra_sections: list[str],
    what         : str,
    context      : str,
):
    plurial = (
        ''
        if len(xtra_sections) == 1 else
        's'
    )

    _xtra_sections = list(xtra_sections)
    _xtra_sections.sort()

    list_xtra_sections = '\n    + '.join(
        s
        for s in [''] + _xtra_sections
    )

    log_raise_error(
        context = context,
        desc    = (
            f'{what.capitalize()} comment section{plurial} used:'
            f"{list_xtra_sections}"
        ),
        exception = ValueError,
    )
