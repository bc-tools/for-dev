#!/usr/bin/env python3

###
# This parser processes lists of python::''TOCPath''-like \specs.
# Paths can be defined relative to a parent folder using a raw
# path, a glob pattern, or a regex pattern, with optional support
# for recursive searches. Here is how each option works.
#
#     1) **Raw paths**must use the \unix path separator (''/''),
#        similar to a URL format.
#
#     1) **\Glob patterns** are indicated using ''glob: ...''
#        (or ''r-glob: ...'' for a recursive search), where
#        ''...'' represents the glob pattern.
#        For example, ''how-to/*.md'' matches all \md files
#        directly inside the path::''how-to'' subfolder.
#
#     1) **\Regex patterns** are indicated using ''regex: ...''
#        (or ''r-regex: ...'' for a recursive search).
#        Note that ''glob: how-to/*.md'' is equivalent to
#        ''r-regex: how-to/[^/]+\.md'', but not to
#        ''regex: how-to/[^/]+\.md''. This is because matching
#        paths inside subfolders requires a recursive directory
#        walk, on which the \regex pattern is then applied.
#
#
# tip::
#     ''g'', ''rg'', ''r'' and ''rr'' are shortcuts for ''glob'',
#     ''r-glob'', ''regex'' and ''r-regex'' respectively.
#
#
# caution::
#     Recursive \regex searches are inefficient because they use
#     a full recursive walk. Recursive glob searches should be
#     more efficient.
#
#
# [[validate]]
#
# Here are the validation steps performed, depending on the kind
# of python::''TOCPath'' defined.
#
#     + A **raw path** must be unbroken (it must point to a valid
#       location).
#
#     + A **pattern (\glob/\regex)** must yield at least one match.
#
#
# note::
#     Parent folder existence is also checked in the background.
#     When working with \aboutmeta, this is unnecessary because
#     the parent folder is always the one containing the
#     path::''''about.yaml'''' file (indeed, this feature is useful
#     when using a standalone python::''TOCPath'' object).
#
#
# [[post-prod+]]
#
# The post-processing returns a \dict with only one key
# ''TAG_POSTPROD_ABOUT_PATH_FILES'' associated to the list of
# "winning" absolute paths build sequentially as follows.
#
#     1) **Raw path file:** a raw path pointing to an existing
#        file is converted to its absolute path and added to
#        the list.
#
#     1) **Raw path directory:** a raw path pointing to an
#        existing folder triggers the creation of a sub-list of
#        absolute paths by parsing the path::''''about.yaml''''
#        file inside that folder (another post-processing step
#        is triggered).
#
#     1) **Winning pattern:** relative paths matched by a
#        pattern are converted to absolute paths and sorted
#        "naturally" using the python::''natsort.natsorted''
#        \func.
#
#
# note::
#     If a raw path points to a non-existent file or folder, or
#     if a pattern yields no matches, an exception will be raised.
###


from natsort import natsorted

from aboutmeta.core.constants.api_tags      import TAG_ATOC
from aboutmeta.core.constants.internal_tags import TAG_PATH_SEP

from aboutmeta.specs.data.toc_path import (
    Path,
    TOCPath,
    TAG_RAW,
)


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     amdata : ''AMData'' instance needed to know the folder
#              of the path::''about.yaml'' file.
#     data   : path \spec or path search pattern provided in
#              the \yaml file.
#
#     :return: ''TOCPath'' instance representing the "extended"
#              path.
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
#     data : ''TOCPath'' object.
#
#     :return: either a string raw path, or a single-key \dict
#              giving the pattern kind as a key, and the pattern
#              itself as the \val.
###
def write(data: TOCPath) -> str | dict[str, str]:
    return data.spec


# --------------- #
# -- POST-PROD -- #
# --------------- #

TAG_POSTPROD_ABOUT_PATH_FILES = '__POSTPROD_ABOUT_PATH_FILES__'


###
# prototype::
#     amdata : :see: parse
#     data   : list of ''TOCPath'' objects.
#
#     :return: \dict with single key
#              ''TAG_POSTPROD_ABOUT_PATH_FILES'' and \val the
#              list of raw and winning pattern absolute paths,
#              validating their existence.
#              Note that for each folder found, an ''AMData''
#              instance is invoked to search for an
#              path::''about.yaml'' file to use for subsequent
#              searches.
#
#
# important::
#     Each group of winning pattern paths is sorted via
#     ''natsort.natsorted'' \func (e.g., path::''script-02.py''
#     precedes path::''script-1.py'').
###
def postprod(
    amdata: object,
    data  : list[TOCPath]
) -> dict[str, list[Path]]:
    paths = []

# Let's walk!
    for tpath in data:
# Raw path.
        if tpath.kind == TAG_RAW:
            full_path = tpath.parent / tpath.pattern

# A folder is treated by a dedicated AMData instance.
            if tpath.pattern[-1] == TAG_PATH_SEP:
                sub_amdata = amdata.new_instance(
                    flavour = TAG_ATOC,
                    parent  = full_path,
                )

                sub_amdata.build()

                results = sub_amdata.postprod()

                paths.extend(
                    results[TAG_POSTPROD_ABOUT_PATH_FILES]
                )

# A file must exists.
            else:
                if not full_path.is_file():
                    raise IOError(
                        f'TOC path {tpath.spec!r} points '
                        f'to missing file:\n{full_path}'
                         "\nSee 'about.yaml' file:\n"
                        f"{amdata.parent}/about.yaml"
                    )

                paths.append(full_path)

# Pattern search. PO is not POO!
        else:
            paths_found = natsorted(tpath.path_iter())

            if not paths_found:
                for k, p in tpath.spec.items(): # Funny Python!
                    ...

                raise ValueError(
                    f"No winning path for the {k} pattern '{p}' "
                    f"inside '{tpath.parent}'."
                )

            paths.extend(paths_found)

# Let's resolve all paths.
    paths = [
        p.resolve()
        for p in paths
    ]

# Nothing left to do.
    return {
        TAG_POSTPROD_ABOUT_PATH_FILES: paths,
    }


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from hypothesis import (
        given,
        strategies as st
    )

    import pytest

    from pathlib import Path

    from aboutmeta.core.temp_dirtree import *

# -- Moke data -- #
    mydirview = """
- readme.md
- script-10.py
- script-02.py
- library:
  - main.py
  - core:
    - readme.md
    - tool.py
    """

    fake_sub_postprod_files = [
        'I.am',
        'danse.le',
        'Mi.a',
    ]

    class MokeAMData:
        @classmethod
        def new_instance(cls, *args, **kwargs):
            return cls(*args, **kwargs)

        def __init__(
            self,
            flavour: str,
            parent : Path,
        ):
            self.flavour = flavour
            self.parent  = parent

        def build(self):
# Mock system does not provide build capabilities.
            ...

        def postprod(
            self,
            keypath: str | list[str] = '',
        ) -> object:
            return {
                TAG_POSTPROD_ABOUT_PATH_FILES: [
                    self.parent / p
                    for p in fake_sub_postprod_files
                ]
            }

# dev:
    from pprint import pprint

    yaml_data = Path(__file__).name

    moke_amdata = MokeAMData(
        flavour = 'fake-flavour',
        parent  = Path('fake-dir'),
    )

    data_parsed = parse(
        amdata = moke_amdata,
        data   = yaml_data
    )

    print("---")
    print(f"{yaml_data          = }")
    print(f"{data_parsed        = }")
    print(f"{write(data_parsed) = }")
# :dev

# -- Back to spec -- #
    @given(
        yaml_data = st.sampled_from([
            Path(__file__).name,
            {'r-glob': "*.py"},
            {'r-regex': r".*\.py"},
        ]),
    )
    def test_back_2_spec(yaml_data: str) -> None:
        moke_amdata = MokeAMData(
            flavour = 'fake-flavour',
            parent  = Path('fake-dir'),
        )

        assert write(
            parse(
                amdata = moke_amdata,
                data   = yaml_data
            )
        ) == yaml_data

    test_back_2_spec()

# -- Post prod -- #
    @given(
        full_data = st.sampled_from([
            (
                ['readme.md'],
                ['readme.md'],
            ),
            (
                [
                    {'rg': '*.py'},
                ],
                [
                    'library/core/tool.py',
                    'library/main.py',
                    'script-02.py',
                    'script-10.py',
                ],
            ),
            (
                [
                    {'g': '*.py'},
                    {'g': '*/*.py'},
                ],
                [
                    'script-02.py',
                    'script-10.py',
                    'library/main.py',
                ],
            ),
            (
                [
                    {'g': '*.py'},
                    'structure/',
                ],
                [
                    'script-02.py',
                    'script-10.py',
                ] + [
                    f'structure/{n}'
                    for n in fake_sub_postprod_files
                ],
            ),
        ]),
    )
    def test_post_prod(full_data: str) -> None:
        yaml_data, paths_wanted = full_data

        with temp_dirtree(mydirview) as tempdir:
            moke_amdata = MokeAMData(
                flavour = 'fake-flavour',
                parent  = tempdir,
            )

            tocpath_list = [
                parse(
                    amdata = moke_amdata,
                    data   = y
                )
                for y in yaml_data
            ]

            paths_found = [
                str(p.relative_to(tempdir))
                for _, paths in postprod(
                    amdata = moke_amdata,
                    data   = tocpath_list,
                ).items()  # Funny Python!
                for p in paths
            ]

        assert paths_found == paths_wanted

    test_post_prod()
