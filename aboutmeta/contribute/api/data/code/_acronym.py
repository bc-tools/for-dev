#!/usr/bin/env python3

from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ------------------ #
# -- DATA MANAGER -- #
# ------------------ #

###
# prototype::
#     spec  : YYYY
#     short : YYYY
#     desc  : YYYY
###
class Acronym(DataManager):
    spec : str
    short: str = field(init = False)
    desc : str = field(init = False)

###
# prototype::
#     :action: derive the ''short'' and ''desc'' attributes from ''self.parts''.
###
    def __post_init__(self):
        parts = []



        return





        self.short = ''
        self.desc  = ''

        return

        extra = []

        for desc_part, accro_part in self.parts:
            self.desc += desc_part

            if not accro_part is None:
                if accro_part != desc_part:
                    extra.append(
                        f"'{accro_part}' for '{desc_part}'"
                    )

                self.short += accro_part

        if extra:
            self.desc += ', with '
            self.desc += ', '.join(extra[:-1])
            self.desc += f' and {extra[-1]}'



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
