#!/usr/bin/env python3

###
# A license is identified using identifiers from the
# cf::{''SPDX'' SPDX License List ; https://spdx.org/licenses/},
# with a certain degree of flexibility. For example, you can type
# ''gpl 3.0+'' and ''cc by nc 4.0'' instead of ''GPL-3.0+'' and
# ''CC-BY-NC-4.0''. More precisely, here is what is allowed.
#
#     1) Spaces can replace hyphens.
#
#     1) Letter case being ignored, you can type everything in
#     lowercase for efficiency.
###


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
    return License(spdx_id = data)


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
def write(data: License) -> str:
    text = data.spdx_id.lower()
    text = text.replace('-', ' ')

    return text


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# We just need some basic interface tests, because we have already
# tested the ''License'' class.

# GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    for yaml_data in [
        "GPL-3.0-only",
        "gpl      -     3.0 only ",
        "cc    by nc 4.0",
        "CC-BY-NC-4.0",
    ]:
        data_parsed = parse(yaml_data)

        print()
        print('~~~')

        print()
        print(f"{yaml_data                 = }")
        print(f"{data_parsed               = }")
        print(f"{write(data_parsed)        = }")
        print(f"{parse(write(data_parsed)) = }")
