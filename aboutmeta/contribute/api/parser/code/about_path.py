#!/usr/bin/env python3

###
# ...
#
#
# [[normalize]]
#
# ...
#
#
# [[validate]]
#
# ...
#
#
# [[post-prod]]
#
# ...
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
#              For each folder found, an ''AMData'' instance
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

# A folder is treated by a dedicated AMData instance.
            if tpath.pattern[-1] == TAG_PATH_SEP:
                sub_amdata = amdata.new_instance(
                    flavour = 'atoc',
                    parent  = full_path,
                )

                paths.extend(sub_amdata.postprod())

# A file must exists.
            else:
                if not full_path.is_file():
                    raise IOError(
                        f'Missing file:\n{full_path}'
                         "\nSee 'about.yaml' file:\n"
                        f"{amdata.parent}/about.yaml"
                    )

                paths.append(full_path)

# Pattern search. PO is not POO!
        else:
            paths.extend(
                natsorted(
                    tpath.path_iter()
                )
            )

# Nothing left to do.
    return paths


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from pprint import pprint

# Moke data
    class MokeAMData:
        @classmethod
        def new_instance(cls, **kwargs):
            return cls(**kwargs)

        def __init__(
            self,
            flavour: str,
            parent : Path,
        ):
            self.flavour = flavour
            self.parent  = parent

        def postprod(
            self,
            keypath: str | list[str] = '',
        ) -> object:
            return [
                self.parent / 'I.am',
                self.parent / 'danse.le',
                self.parent / 'Mi.a',
            ]


    projdir = filedir = Path(__file__).parent

    while projdir.name != 'aboutmeta':
        projdir = projdir.parent

# # GOOD
#     moke_amdata = MokeAMData(
#         flavour = 'atoc',
#         parent  = filedir,
#     )

#     print()
#     print("-- GOOD CASES --")

#     for yaml_data in [
#         Path(__file__).name,
#         {'rg': "*.py"},
#         {'rr': r".*\.py"},
#     ]:
#         print()
#         print('~~~')

#         data_parsed = parse(
#             amdata = moke_amdata,
#             data   = yaml_data
#         )

#         print()
#         print(f"{yaml_data          = }")
#         print(f"{data_parsed        = }")
#         print(f"{write(data_parsed) = }")

# POST PROD - GOOD
    moke_amdata = MokeAMData(
        flavour = 'atoc',
        parent  = (
              projdir
            / 'contribute' / 'api' / 'parser' / 'readme'
        ),
    )

    print()
    print("-- POST PROD - GOOD CASES --")

    print()

    tocpath_list = [
        parse(
            amdata = moke_amdata,
            data   = y
        )
        for y in [
            'title.md',
            {'g': 'how-to/*.md'},
            'structure/',
        ]
    ]

    print('spec list')
    pprint([
        tp.spec
        for tp in tocpath_list
    ])

    print()
    print('RELATIVE PATH list')
    pprint([
        p.relative_to(projdir)
        for p in postprod(
            amdata = moke_amdata,
            data   = tocpath_list,
        )
    ])

# # POST PROD - BAD
#     exit()
#     print()
#     print("-- POST PROD - GOOD CASES --")

#     amdata = AMData()
#     amdata.parent = Path(__file__).parent

#     while amdata.parent.name != 'aboutmeta':
#         amdata.parent = amdata.parent.parent

#     amdata.parent = (
#         amdata.parent
#         / 'contribute' / 'api' / 'data' / 'readme'
#     )

#     print()
#     print('~~~')

#     yaml_list = [
#         parse(
#             amdata = amdata,
#             data   = y)
#         for y in [
#             'README.md',
#             {'g': 'code/*.py'},
#         ]
#     ]

#     print()
#     print('YAML list')
#     pprint(yaml_list)

#     print()
#     print('RELATIVE PATH list')
#     pprint([
#         p.relative_to(amdata.parent)
#         for p in postprod(yaml_list)
#     ])
