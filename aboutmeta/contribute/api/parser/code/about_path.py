#!/usr/bin/env python3

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
    TAG_TOC_GLOB_PATTERNS,
    TAG_GLOB_METHOD,
    TAG_GLOB_RECU_METHOD,
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


# ------------- #
# -- MAPPERS -- #
# ------------- #

###
# prototype::
#     amdata   : :see: parse
#     tocpaths : a list of ''TOCPath'' object.
#
#     :return: the list of raw paths and winning pattern paths
#              found. Raises an error if a path does not exist.
#
#
# note::
#     Each group of paths found using a pattern are sorted by
#     the function ''natsort.natsorted''.
###
def post_prod(
    amdata: object,
    data  : list[TOCPath]
) -> list[Path]:
    ...

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


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from aboutmeta.amdata import AMData

    from pprint import pprint

# GOOD
    print()
    print("-- GOOD CASES --")

    amdata = AMData()
    amdata.parent = Path(__file__).parent

    for yaml_data in [
        Path(__file__).name,
        {'rg': "*.py"},
        {'rr': r".*\.py"},
    ]:
        print()
        print('~~~')

        data_parsed = parse(
            amdata = amdata,
            data   = yaml_data
        )

        print()
        print(f"{yaml_data          = }")
        print(f"{data_parsed        = }")
        print(f"{write(data_parsed) = }")

# MAP LIST - GOOD
    print()
    print("-- MAP LIST - GOOD CASES --")

    amdata = AMData()
    amdata.parent = Path(__file__).parent

    while amdata.parent.name != 'aboutmeta':
        amdata.parent = amdata.parent.parent

    amdata.parent = (
        amdata.parent
        / 'contribute' / 'api' / 'data' / 'readme'
    )

    print()
    print('~~~')

    yaml_list = [
        parse(
            amdata = amdata,
            data   = y)
        for y in [
            'title.md',
            {'g': 'how-to/*.md'},
            'structure/',
        ]
    ]

    print()
    print('YAML list')
    pprint(yaml_list)

    print()
    print('RELATIVE PATH list')
    pprint([
        p.relative_to(amdata.parent)
        for p in map_list(yaml_list)
    ])

# MAP LIST - BAD
    exit()
    print()
    print("-- MAP LIST - GOOD CASES --")

    amdata = AMData()
    amdata.parent = Path(__file__).parent

    while amdata.parent.name != 'aboutmeta':
        amdata.parent = amdata.parent.parent

    amdata.parent = (
        amdata.parent
        / 'contribute' / 'api' / 'data' / 'readme'
    )

    print()
    print('~~~')

    yaml_list = [
        parse(
            amdata = amdata,
            data   = y)
        for y in [
            'README.md',
            {'g': 'code/*.py'},
        ]
    ]

    print()
    print('YAML list')
    pprint(yaml_list)

    print()
    print('RELATIVE PATH list')
    pprint([
        p.relative_to(amdata.parent)
        for p in map_list(yaml_list)
    ])
