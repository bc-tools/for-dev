#!/usr/bin/env python3

###
# A language is indicated using the cf::''ISO 639 standard ;
# https://en.wikipedia.org/wiki/ISO_639'' short identifier, then,
# if necessary, add a country using the cf::''ISO 3166 standard ;
# https://en.wikipedia.org/wiki/ISO_3166'' classifier.
# For example, ''fr'' indicates France French, whereas ''fr-BE''
# indicates Belgian French.
#
#
# important::
#     The default language is ''en-US'' for US English.
#
#
# tip::
#     You can use ''_'' instead of ''-''. This can be useful when
#     pasting external text or more efficient when typing.
###


from aboutmeta.specs.data.lang import Lang


# ------------ #
# -- PARSER -- #
# ------------ #

###
# prototype::
#     data : the \lang provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''Lang''.
###
def parse(data: str) -> Lang:
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.lang.Lang''.
    return Lang(std_id = data)


# ------------ #
# -- WRITER -- #
# ------------ #

###
# prototype::
#     data : a ''Lang'' object.
#
#     :return: the standard \yaml version of the ''Lang'' object
#              which is the full language identifier.
###
def write(data: Lang) -> str:
    return data.std_id


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# We just need some basic interface tests, because we have already
# tested the ''Lang'' class.

# GOOD
    print()
    print("-- GOOD CASES --")

    std_yaml_data = "fr"
    data_parsed   = parse(std_yaml_data)

    print()
    print('~~~')

    print()
    print(f"{std_yaml_data = }")

    print()
    print(repr(data_parsed))

    std_yaml_data = write(data_parsed)

    print()
    print(f"{std_yaml_data = }")
