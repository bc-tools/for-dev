#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/about_path.py'


###
# ???
###


from natsort import natsorted


from aboutmeta.amdata import AMData

from aboutmeta.specs.data.tocpath import (
    Path,
    TOCPath,
    TAG_TOC_PATH_RAW,
    TAG_TOC_GLOB_PATTERNS,
    TAG_GLOB_METHOD,
    TAG_GLOB_RECU_METHOD
)


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     amdata : an instance of ''AMData'' needed to know the folder
#              of the path::''about.yaml'' file.
#     data   : the specification of a path or a search pattern
#              for paths.
#
#     :return: an instance of the class ''TOCPath'' to work
#              easily with the license.
###
def parse(
    amdata: AMData,
    data  : str
) -> TOCPath:
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.tocpath.TOCPath''.
    return TOCPath(
        spec   = data,
        parent = amdata.parent
    )


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''License'' object.
#
#     :return: either a string raw path, or a dictionary giving
#              the kind of pattern as a key, and the pattern
#              itself as the value of the single key.
###
def write(data: TOCPath) -> str | dict[str, str]:
    return data.spec


# ------------- #
# -- MAPPERS -- #
# ------------- #

TAG_PATH_SEP   = '/'
TAG_ABOUT_YAML = 'about.yaml'


###
# prototype::
#     tocpaths : a list of ''TOCPath'' object.
#
#     :return: the list of the raw paths and wining pattern paths
#              found.
#
#
# note::
#     The paths found using a pattern are sorted by the function
#     ''natsort.natsorted''.
###
# def map_list(tocpaths: list[TOCPath]) -> list[Path]:
#     TODO


#     paths = []

# # Let's walk!
#     for tpath in tocpaths:
#         kind = tpath.kind

# # Raw path.
#         if kind == TAG_TOC_PATH_RAW:
#             full_path = tpath.parent / tpath.pattern

# # A file must exists.
#             if tpath.pattern[-1] != TAG_PATH_SEP:
#                 if not full_path.is_file():
#                     raise IOError(
#                         f'Not found file:\n{full_path}'
#                     )


# # A folder must contain an ''about.yaml'' file.
#             else:
#                 sub_about_file = full_path / TAG_ABOUT_YAML

#                 if not sub_about_file.is_file():
#                     raise IOError(
#                         f"Missing ''{TAG_ABOUT_YAML}'' file inside a folder:\n{full_path}"
#                     )


# # Let's store the new path(s).
#             paths.append(
#                 tpath.parent / tpath.pattern
#             )

# # Pattern search.
#         else:
#             glob_method_name = (
#                 TAG_GLOB_METHOD
#                 if tpath._is_recu_search() else
#                 TAG_GLOB_RECU_METHOD
#             )

#             iterator_name = (
#                 'glob_iter'
#                 if kind in TAG_TOC_GLOB_PATTERNS else
#                 'regex_iter'
#             )

#             paths += natsorted(
#                 list(
#                     getattr(
#                         tpath,
#                         iterator_name
#                     )(glob_method_name)
#                 )
#             )

# # Nothing left to do.
#     return paths
