# ------------- #
# -- IMPORTS -- #
# ------------- #

from semver import (
    Version,
    VersionInfo,
)


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : the \nbver provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''semver.Version'' to work
#              easily with the number version.
###
def parser(content: str) -> Version:
    version = VersionInfo.parse(content)

    return version
