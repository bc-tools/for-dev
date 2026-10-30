#!/usr/bin/env python3

# Code extracted from the maintained Python file
# 'aboutmeta/contribute/api/parser/code/sem_version.py'


###
# Semantic version \nbs must comply with cf::''Semantic
# Versioning ; https://semver.org/'' like nbver::''1.0.0'',
# nbver::''0.0.0-beta.1'', and nbver::''0.3.1-beta.1+build.5''.
###


from semver import (
    Version,
    VersionInfo,
)

from aboutmeta.core.errors import ParsingError


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : the \nbver provided in the \yaml file, but stripped.
#
#     :return: an instance of the ''semver.Version'' class
#              representing the \nbver.
###
def parse(data: str) -> Version:
    try:
        version = VersionInfo.parse(data)

    except ValueError as e:
        raise ParsingError(e)

    return version


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''semver.Version'' object.
#
#     :return: the \std \yaml version of the ''semver.Version''
#              object.
###
def write(data: Version) -> str:
    return str(data)
