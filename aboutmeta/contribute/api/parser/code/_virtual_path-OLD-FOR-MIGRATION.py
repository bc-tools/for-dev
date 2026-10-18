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
    ...

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


# ------------- #
# -- MAPPERS -- #
# ------------- #

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


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# BAD
    BAD = True
    BAD = False

    if BAD:
        pseudopath = "../../../"
        pseudopath = "ap.md"
        pseudopath = ['glob', "*.md"]
        pseudopath = {'glob': "*.md", 'regex': r".*/pr.*\.md"}
        pseudopath = {'glb': "*.md"}
        pseudopath = {'regex': r".*(pr"}

        parse(readme_dir, pseudopath)

# MAP LIST
    from aboutmeta.amdata import AMData

    folder = readme_dir.parent

    paths = map_list(
        AMData,
        [parse(folder, "readme/")]
    )

    for p in paths:
        try:
            p = p.relative_to(folder)
        except:
            ...

        print(f"+ {p}")
