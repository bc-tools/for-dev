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
    url_data = URL(
        yaml_val = data,
        url      = data
    )

# We must normalize the ''url'' attribute.
    url_data.normalize()

    return url_data


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# We just need some basic interface tests, because we have already
# tested the ''URL'' class.

# GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    mydata_paresed = parse("HTTPS://QwAnT.com")

    print(repr(mydata_paresed))
    print(f"{mydata_paresed.url = }")

# BAD
    # exit()

    print("\n------------\n")

    print("-- BAD CASES --")

    try:
        parse(42)

    except Exception as e:
        print(type(e).__name__, ':', e)
