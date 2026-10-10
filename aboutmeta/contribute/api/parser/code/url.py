#!/usr/bin/env python3

from aboutmeta.specs.data.url import URL


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : one \url provided in the \yaml file, but stripped.
#
#     :return: an exact copy of the data.
#
#
# note::
#     The sole purpose of this fake parser is to generate an
#     internal ''URL'' class that can be used to validate
#     and normalize a URL.
###
def parse(data: str) -> URL:
# No parsing, and all job done by ''aboutmeta.specs.data.url.URL''.
    return URL(url = data)


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# We just need some basic interface tests, because we have already
# tested the ''URL'' class.

# GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    print()

    str_data    = "HTTPS://QwAnT.com"
    data_parsed = parse(str_data)

    print(str_data)
    print(repr(data_parsed))

# BAD
    # exit()

    print("\n------------\n")

    print("-- BAD CASES --")

    print()

    try:
        str_data = 42

        print(str_data)
        parse(str_data)

    except Exception as e:
        print(type(e).__name__, ':', e)
