#!/usr/bin/env python3

###
# XXXXXXX
# XXXXXXX
# XXXXXXX
# XXXXXXX
# XXXXXXX
# XXXXXXX
# XXXXXXX
# XXXXXXX



#   The special zero-argument method `normalize` is used to normalize attribute values. For example, the `url.URl.normalize` can be used to obtain a URL in its standard form (this fairly flexible format accepts different forms for the same URL).

#
#
# note::
#     URLs are never verified automatically, but they can be validated
#     on demand (technically, this requires an internet connection, so
#     it is not possible to validate a URL every time an ''about.yaml''
#     file is analyzed).*
#
# Here are the normalizations done.
#
#     1. Some valid \url_s use typographical quirks.
#     For example, ''HTTPS://QwAnT.com'' is valid, but its
#     normalized version is ''https://qwant.com''.
#
#     1. Special \html character encoding is also handled.
#     For example, ''http://abc.com/Dôssier Testé.html''
#     becomes ''http://abc.com/D%C3%B4ssier%20Test%C3%A9.html''.
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
