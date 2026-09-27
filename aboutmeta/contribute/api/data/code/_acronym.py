#!/usr/bin/env python3

from aboutmeta.core.data_manager import DataManager


# ------------------- #
# -- MY DATA CLASS -- #
# ------------------- #

###
# prototype::  A REVOIR
#     short : the acronym
#     full  : the full text
#     parts : XXX  parties définissant l'acronyme, PB on fige trop le syst,donc on doit avoir une sosu classe pour gerer le type de texte
###
class Acronym(DataManager):
    short: str
    full : str
    parts


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Nothing to test!
    ...
