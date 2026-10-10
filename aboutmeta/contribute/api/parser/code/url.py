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


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a `URL` data.
#
#     :return: the standard `YAML` version of the `Person` data.
###
def write(data: URL) -> str:
    return data.url


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# We just need some basic interface tests, because we have already
# tested the ''URL'' class.

# GOOD
    print()
    print("-- GOOD CASES --")

    str_data    = "HTTPS://QwAnT.com"
    data_parsed = parse(str_data)

    print()
    print('~~~')

    print()
    print(f"{str_data = }")

    print()
    print(repr(data_parsed))

    std_yaml_data = write(data_parsed)

    print()
    print(f"{std_yaml_data = }")

# BAD
    # exit()

    # print()
    # print("-- BAD CASES --")

    # str_data = '42'

    # print()
    # print(f"{str_data = }")

    # try:
    #     parse(str_data)

    # except Exception as e:
    #     print(type(e).__name__, ':', e)
