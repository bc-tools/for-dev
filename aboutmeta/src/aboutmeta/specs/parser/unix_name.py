#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/unix_name.py'


###
# A Unix-style name only uses lowercase letters, digits,
# underscores, and hyphens, and cannot start with a digit
# or a hyphen.
###


from aboutmeta.specs.data.unix_name import UnixName


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : a Unix name provided in the \yaml file, but
#            stripped.
#
#     :return: an instance of the ''UnixName'' class.
###
def parse(data: str) -> UnixName:
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.unix_name.UnixName''.
    return UnixName(name = data)


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''UnixName'' object.
#
#     :return: the standard \yaml version of the ''UnixName''
#              object.
###
def write(data: UnixName) -> str:
    return data.name
