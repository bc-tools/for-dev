#!/usr/bin/env python3

from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ------------------ #
# -- DATA MANAGER -- #
# ------------------ #

###
# prototype::  A REVOIR
#     XXX : YYYY
#
#
# "[about] [meta]data" stored as
#     + parts = (
#         ("about", "about"),
#         (" "    , None),
#         ("meta" , "meta"),
#         ("data" , None),
#     )
#     + short = "aboutmeta"
#     + desc  = "about metadata"
#
#
# "[about=@-]    [meta=met@]data" stored as
#     + parts = (
#         ("about", "@-" ),
#         (" "    , None),
#         ("meta" , "met@"),
#         ("data" , None),
#     )
#     + short = "@-met@"
#     + desc  = "about metadata, with '@' for 'about' and 'meta' for 'met@'"
###
class Acronym(DataManager):
    parts: tuple((str, str | None))
    short: str = field(init = False)
    desc : str = field(init = False)

###
# prototype::
#     :action: derive the ''short'' and ''desc'' attributes from ''self.parts''.
###
    def __post_init__(self):
        self.short = ''
        self.desc  = ''

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

    for parts in [
        (
            ("about", "about" ),
            (" "    , None),
            ("meta" , "meta"),
            ("data" , None),
        ),
        (
            ("about", "@-" ),
            (" "    , None),
            ("meta" , "met@"),
            ("data" , None),
        ),
    ]:
        mydata = Acronym(parts = parts)

        print()
        print(f"{parts  = }")
        print(f"{mydata = }")
