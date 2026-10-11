#!/usr/bin/env python3

from aboutmeta.specs.data.license import License


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : the \lic code provided in the \yaml file, but
#            stripped.
#
#     :return: an instance of the class ''License'' to work
#              easily with the license.
###
def parse(data: str) -> License:
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.license.License''.
    return License(identifier = data)


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''License'' object.
#
#     :return: a human-friendly, standard \yaml representation
#              of the ''License'' object, with a \spdx lowercase
#              identifier and spaces instead of hyphens.
###
def write(data: License) -> str:
    text = data.identifier.lower()
    text = text.replace('-', ' ')

    return text


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
   # GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    for std_yaml_data in [
        "gpl      -     3.0 only ",
        "cc    by nc 4.0",
    ]:
        data_parsed = parse(std_yaml_data)

        print()
        print('~~~')

        print()
        print(f"{std_yaml_data = }")

        print()
        print(repr(data_parsed))

        std_yaml_data = write(data_parsed)

        print()
        print(f"{std_yaml_data = }")
