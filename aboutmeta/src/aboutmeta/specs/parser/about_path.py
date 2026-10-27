#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/about_path.py'


###
# ???
###


from natsort import natsorted

from aboutmeta.core.constants import (
    TAG_PATH_SEP,
    TAG_ABOUT_YAML,
)

from aboutmeta.specs.data.toc_path import (
    Path,
    TOCPath,
    TAG_TOC_PATH_RAW,
    ParsingError,
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
    amdata: object,
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


# --------------- #
# -- POST-PROD -- #
# --------------- #

###
# prototype::
#     amdata : :see: parse
#     data   : a list of ''TOCPath'' object.
#
#     :return: the list of raw and winning pattern paths,
#              validating their existence.
#              For each directory found, an ''AMData'' instance
#              is invoked to search for path::''about.yaml''
#              files to use for subsequent searches.
#
#
# note::
#     Each group of winning pattern paths found using a pattern
#     are sorted by the function ''natsort.natsorted''.
###
def postprod(
    amdata: object,
    data  : list[TOCPath]
) -> list[Path]:
    paths = []

# Let's walk!
    for tpath in data:
# Raw path.
        if tpath.kind == TAG_TOC_PATH_RAW:
            full_path = tpath.parent / tpath.pattern

# A file must exists.
            if tpath.pattern[-1] != TAG_PATH_SEP:
                if not full_path.is_file():
                    raise IOError(
                        f'Missing file:\n{full_path}'
                         "\nSee 'about.yaml' file:\n"
                        f"{amdata.parent}/about.yaml"
                    )

                paths.append(full_path)

# A folder is treated by a dedicated AMData instance.
            else:
                sub_amdata = amdata.new_instance(
                    flavour = 'atoc',
                    parent  = full_path,
                )

                paths += sub_amdata.postprod('atoc')

# Pattern search.
        else:
            ...

# Nothing left to do.
    return paths













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
