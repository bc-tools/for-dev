#!/usr/bin/env python3

###
# All valid URLs are accepted like the ugly ''HTTPS://QwAnT.com''
# or the human friendly 'http://abc.com/Dôssier Testé.html''
# instead of the standard URLs ''https://qwant.com'' and
# ''http://abc.com/D%C3%B4ssier%20Test%C3%A9.html'' respectively.
#
#
# [[normalize]]
# ...
#
#
# [[validate]]
# ...
###

from aboutmeta.specs.data.url import URL


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : one \url provided in the \yaml file, but stripped.
#
#     :return: an instance of the ''URL'' class.
###
def parse(data: str) -> URL:
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.url.URL''.
    return URL(url = data)


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''URL'' object.
#
#     :return: the standard \yaml version of the ''URL'' object.
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

    std_yaml_data = "HTTPS://QwAnT.com"
    data_parsed   = parse(std_yaml_data)

    print()
    print('~~~')

    print()
    print(f"{std_yaml_data = }")

    print()
    print(repr(data_parsed))

    std_yaml_data = write(data_parsed)

    print()
    print(f"{std_yaml_data = }")
