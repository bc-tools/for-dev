#!/usr/bin/env python3

import re

from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ------------------ #
# -- DATA MANAGER -- #
# ------------------ #

_PATTERN_ACRONYM_METADATA = re.compile(
    r'\[\s*(.*?)(?:\s*::\s*(.*?))?\s*\]|([^\[]+)'
)


###
# prototype::
#     spec  : YYYY
#     short : YYYY
#     desc  : YYYY
#
#
# note::
#     The ''short'' and ''desc'' attributes are build from the
#     value of the ''spec'' attribute.
###
class Acronym(DataManager):
    spec : str
    short: str = field(init = False)
    desc : str = field(init = False)

###
# prototype::
#     :action: derive the ''short'' and ''desc'' attributes from
#              ''self.spec''.
###
    def __post_init__(self):



        return


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    for spec in [
        "[about] [meta]data",
        "[about::@-]     [meta   ::   met-@]data",
    ]:
        mydata = Acronym(spec = spec)

        print()
        print(f"{spec   = }")
        print(f"{mydata = }")



exit()


# Exemple avec un '::' absent dans le deuxième crochet
texte = "[about::@-]      [meta]data"

# Expression régulière :
# 1. Capture un bloc entre crochets avec optionnellement '::' et une valeur


resultat = []

for match in re.finditer(pattern, texte):
    part1, part2, other = match.groups()

    if part1 is not None:
        key = part1.strip()
        # Si '::' était présent, part2 contient la valeur, sinon on réutilise key
        val = part2.strip() if part2 is not None else key
        resultat.append((key, val))
    elif other is not None:
        # Texte ou espaces en dehors des crochets
        resultat.append((other, None))

print(resultat)
