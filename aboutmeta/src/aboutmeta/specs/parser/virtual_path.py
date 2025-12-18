#####################################
# TOUT REPRENDRE ! CHGTS VIA DICT PATTERNS MAL PRIS EN COMPTE + CHGT BRUTALE DE parent


#!/usr/bin/env python3

from pathlib import Path
import              re

from natsort import natsorted

from aboutmeta.core.constants     import *
from aboutmeta.core.errors        import ParsingError
from aboutmeta.specs.data.tocpath import TOCPath


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TOCPathList = list[TOCPath]


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     amdata_cls : an instance of the class ''amdata.AMData''
#                  (this is needed to access to the folder of
#                  the path::''about.yaml'' file).
#     data       : a virtual path that is either a relative path
#                  in the form of a string, or a pattern, using
#                  the \glob or \regex syntax, with the patterns
#                  provided using a single-key \dict.
#
#     :return: an instance of the ''TOCPath'' class that allows
#              subsequent anlysis of a new path::''about.yaml''
#              file if necessary.
#
#
# Let's look at some virtual examples where we assume that the
# yaml file folder has absolute path path::''/abs/path/readme''.
#
#
# [[An existing file]]
#
# Let's assume that the file path ::''/abs/path/readme/api.md''
# exists. In this case, using ''data = "api.md"'' will imply the
# return of the following ''TOCPath'' \obj. The use of a list
# can be understood by looking at the paths returned when using
# \glob or \regex patterns (see below).
#
# python::
#     TOCPath(
#         std        = 'api/md',
#         postsearch = None,
#         paths      = [PosixPath('/abs/path/readme/api.md')])
#
#
# [[An existing folder]]
#
# Let's assume that the folder path ::''/abs/path/readme/api''
# exists. In this case, using ''data = "api/"'' will imply the
# return of the following ''TOCPath'' \obj indicating that the
# yaml::''toc'' block of an path::''about.yaml'' file need to
# be analyzed during of post action.
#
# python::
#     TOCPath(
#         std        = 'api/',
#         postsearch = PosixPath('/abs/path/readme/api/about.yaml',
#         paths      = [])
#
#
# [[A "flat" \glob pattern]]
#
# If ''data = {'glob': "*.md"}'' is used, and the \glob pattern
# finds paths, then something like the following ''TOCPath''
# \obj can be returned, the list being sorted "naturally" via
# ''natsort'' module.
#
# python::
#     TOCPath(
#         std        = "glob: '*.md'",
#         postsearch = None,
#         paths      = [PosixPath('/abs/path/readme/about.md'),
#                       PosixPath('/abs/path/readme/api.md'),
#                       PosixPath('/abs/path/readme/specs.md')])
#
#
# [[A "recursive" \glob pattern]]
#
# If ''data = {'r-glob': "*.md"}'' is used, and the search will
# be done recursively giving something like the ''TOCPath'' \obj
# below.
#
# python::
#     TOCPath(
#         std        = "r-glob: '*.md'",
#         postsearch = None,
#         paths      = [PosixPath('/abs/path/readme/about.md'),
#                       PosixPath('/abs/path/readme/api.md'),
#                       PosixPath('/abs/path/readme/api/extract.md'),
#                       PosixPath('/abs/path/readme/api/use.md'),
#                       PosixPath('/abs/path/readme/api/use/project.md'),
#                       PosixPath('/abs/path/readme/api/use/toc.md'),
#                       PosixPath('/abs/path/readme/api/validate.md'),
#                       PosixPath('/abs/path/readme/api/validate/email.md'),
#                       PosixPath('/abs/path/readme/api/validate/url.md'),
#                       PosixPath('/abs/path/readme/deps.md')])
#
#
# [[\regex patterns]]
#
# You can use \regexs for more advanced needs. The first \glob
# pattern can be rewritten as ''data = {'regex': r".*\.md"}'',
# and the second one as ''data = {'r-regex': r".*\.md"}''.
###
def parse(
    amdata_cls: object,
    data      : str | dict[str, str]
) -> TOCPath:
    about_file_dir = amdata_cls.yaml_file_dir

# A "direct" path?
    if isinstance(data, str):
        return _parse_direct_path(about_file_dir, data)

# A legal pattern?
    if not isinstance(data, dict):
        _raisethis(
            about_file_dir  = about_file_dir,
            data            = data,
            message         = (
                "one dict expected for one glob or regex pattern."
            )
        )

    if not len(data.keys()) == 1:
        _raisethis(
            about_file_dir  = about_file_dir,
            data            = data,
            message         = (
                "one single key expected for a pattern dict."
            )
        )

# Let's work with a single pattern.
    for kind, pattern in data.items(): # Python is funny...
        ...

    return _parse_pattern(about_file_dir, data, kind, pattern)


###
# prototype::
#     about_file_dir : a well named \arg.
#     data           : :see: parse
#     kind           : the main error message.
#     xtra           : complementary information printed as an
#                      item.
#
#     :action: raise errors.
###
def _raisethis(
    about_file_dir: Path,
    data          : str | dict[str, str],
    message       : str,
    xtra          : str = ""
) -> None:
    if xtra:
        xtra = f"    + {xtra}"

    raise ParsingError(
        f"""
{message}
    + DATA: {data!r}
    + FILE: {about_file_dir}/about.yaml
{xtra}
        """.strip()
    )


###
# prototype::
#     data : :see: parse
#
#     :return: the \std value for the path::''about.yaml'' file.
###
def _std(data: str | dict[str, str]) -> str:
# One-key dict used in the initial ''YAML'' file.
    if isinstance(data, dict):
        for k, v in data.items():
            return f"{k}: {v!r}"

# One string used in the initial ''YAML'' file.
    return data


###
# prototype::
#     about_file_dir : a well named \arg.
#     data           : :see: parse
#
#     :return: :see: parse
###
def _parse_direct_path(
    about_file_dir: Path,
    data          : str
) -> TOCPath:
    is_dir = bool(data[-1] == "/")

# Just a "full" path resolved is useful.
    fullpath = about_file_dir / Path(data)
    fullpath = fullpath.resolve()

# Folder for an ''about.yaml'' file?
    if is_dir:
        if not fullpath.is_dir():
            _raisethis(
                about_file_dir = about_file_dir,
                data           = data,
                message        = "inexistant folder.",
                xtra           = f"FOLDER: {fullpath}"
            )

        sub_yaml_file = fullpath / "about.yaml"

        if not sub_yaml_file.is_file():
            _raisethis(
                about_file_dir = about_file_dir,
                data           = data,
                message        = (
                    "folder without an ''about.yaml'' file."
                ),
                xtra           = f"FOLDER: {fullpath}"
            )

        postsearch = sub_yaml_file
        paths      = []

# File?
    else:
        if not fullpath.is_file():
            _raisethis(
                about_file_dir  = about_file_dir,
                data            = data,
                message         = "path not pointing to a file."
            )

        postsearch = None
        paths      = [fullpath]

# "Direct" path looks good.
    return TOCPath(
        std        = _std(data),
        postsearch = postsearch,
        paths      = paths
    )


###
# prototype::
#     about_file_dir : :see: parse
#     data           : :see: parse
#     kind           : the kind of pattern.
#                    @ kind in [
#                          "glob", "r-glob",
#                          "regex", "r-regex"
#                      ]
#     pattern        : the pattern.
#
#     :return: :see: parse
###
def _parse_pattern(
    about_file_dir: Path,
    data          : dict[str, str],
    kind          : str,
    pattern       : str
) -> TOCPath:
# Legal key?
    kind = TAG_TOC_PATTERN_ABBREV.get(kind, kind)

    if not kind in TAG_TOC_PATTERN_KINDS:
        _raisethis(
            about_file_dir = about_file_dir,
            data           = data,
            message        = f"illegal pattern kind ''{kind}''."
        )

# User has used an abbreviationthat we don't keep in the standard
# version of the data.
    if not kind in data:
        data = {kind: pattern}

# ''glob'' pattern.
    if kind in TAG_TOC_GLOB_PATTERNS:
        _glob = "glob"

        if kind == TAG_TOC_PATH_RECU_GLOB:
            _glob = f"r{_glob}"

        paths = [
            p
            for p in getattr(about_file_dir, _glob)(pattern)
            if p.is_file()
        ]

# ''regex'' pattern.
    else:
        try:
            pattern = re.compile(pattern)

        except re.error as e:
            _raisethis(
                about_file_dir = about_file_dir,
                data           = data,
                message        = (
                    f"regex compilation failed for {pattern!r}."
                ),
                xtra           = f"REGEX ERROR: {e}"
            )

        paths = []

        _glob = "glob" if kind == "regex" else "rglob"

        for fullpath in getattr(about_file_dir, _glob)("*"):
            relpath = fullpath.relative_to(about_file_dir)

            if pattern.fullmatch(str(relpath)):
                paths.append(fullpath)

# Loosing pattern?
    if not paths:
        _raisethis(
            about_file_dir = about_file_dir,
            data           = data,
            message        = f"no files found with the pattern."
        )

# Winning pattern.
    return TOCPath(
        std        = _std(data),
        postsearch = None,
        paths      = natsorted(paths)
    )


# ------------ #
# -- MAPPER -- #
# ------------ #

###
# prototype::
#     amdata_cls : the ''AMData'' class, which will be instantiated
#                  to search recursively for files.
#     data_list  : a ''TOCPath'' list.
#
#     :return: the list obtained from ''data_list'' by adding any
#              files from the analysis of path::''about.yaml'' files
#              (cf. the folders indicated in the ''toc'' blocks).
###
def map_list(
    amdata_cls: object,
    data_list : TOCPathList
) -> TOCPathList:
    final_paths = []

    for data in data_list:
        if data.paths:
            final_paths += data.paths

        else:
            _amdata = amdata_cls(flavour = "toc")
            _amdata.build(yaml_file = data.postsearch)

            final_paths += _amdata.data.toc

    return final_paths
