# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.data import url


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : one \url provided in the \yaml file, but stripped.
#
#     :return: an exact copy of the content.
#
#
# note::
#     This fake parser greatly simplifies the part that handles
#     validations.
###
def parser(content: str) -> url.URL:
# We do almost nothing...
    return url.URL(url = content)
