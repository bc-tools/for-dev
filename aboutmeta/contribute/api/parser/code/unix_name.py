#!/usr/bin/env python3

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
def yamlify(data: UnixName) -> str:
    return data.name


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# We just need some basic interface tests, because we have already
# tested the ''UnixName'' class.

# GOOD
    print()
    print("-- GOOD CASES --")

    yaml_data   = "_abc-cde123"
    data_parsed = parse(yaml_data)

    print()
    print('~~~')

    print()
    print(f"{yaml_data            = }")
    print(f"{data_parsed          = }")
    print(f"{yamlify(data_parsed) = }")
