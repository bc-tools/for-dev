#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/licensing.py'


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


from aboutmeta.specs.data.licensing import Licensing


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : the \lic code provided in the \yaml file, but
#            stripped.
#
#     :return: an instance of the class ''Licensing'' to work
#              easily with the license.
###
def parse(data: str) -> Licensing:
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.license.License''.
    return Licensing(spdx_id = data)


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''Licensing'' object.
#
#     :return: a human-friendly, standard \yaml representation of
#              the ''License'' object: this is the \spdx lowercase
#              identifier and spaces instead of hyphens.
###
def write(data: Licensing) -> str:
    text = data.spdx_id.lower()
    text = text.replace('-', ' ')

    return text
