#!/usr/bin/env python3

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
#     :return: an instance of the class ''semver.Version'' to work
#              easily with the number version.
###
def parse(data: str) -> Version:
    try:
        version = VersionInfo.parse(data)

    except ValueError as e:
        raise ParsingError(e)

    return version
