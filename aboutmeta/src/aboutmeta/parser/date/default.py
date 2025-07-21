# ------------- #
# -- IMPORTS -- #
# ------------- #

from datetime import datetime


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : the date provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''datetime.date'' to work
#              easily with the date.
###
def parser(content: str) -> datetime.date:
    d = datetime.strptime(content, "%Y-%m-%d").date()

    return d
