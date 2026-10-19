#!/usr/bin/env python3

###
# ???
###


from natsort import natsorted


from aboutmeta.amdata import AMData

from aboutmeta.specs.data.tocpath import (
    Path,
    TOCPath,
    TAG_TOC_PATH_RAW,
    TAG_TOC_GLOB_PATTERNS
)


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     amdata : an instance of ''AMData'' needed to know the parent
#              directory.
#     data   : the specification of a path or search pattern for
#              paths.
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
#     :return: a human-friendly, standard \yaml representation of
#              the ''License'' object: this is the \spdx lowercase
#              identifier and spaces instead of hyphens.
###
def write(data: TOCPath) -> str | dict[str, str]:
    return data.spec


# ------------- #
# -- MAPPERS -- #
# ------------- #

def map_list():
    ...


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# We just need some basic interface tests, because we have already
# tested the ''Person'' class.

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
