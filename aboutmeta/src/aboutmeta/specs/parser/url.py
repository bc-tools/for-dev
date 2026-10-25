#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/url.py'


###
# All valid URLs are accepted.
#
#
# [[normalize]]
# Here are the normalizations done.
#
#     1. Typographical quirks are removed. For example,
#     ''HTTPS://QwAnT.com'' becomes ''https://qwant.com''.
#
#     1. Special HTML character encoding is handled. For
#     example, ''http://abc.com/Dôssier Testé.html'' becomes
#     ''http://abc.com/D%C3%B4ssier%20Test%C3%A9.html''.
#
#
# [[validate]]
# URL validation uses DNS to check for the existence of the
# hostname, while HTTP techniques verify its online availability.
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
