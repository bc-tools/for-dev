#!/usr/bin/env python3


# -------------------------- #
# -- TRANSFORMING STRINGS -- #
# -------------------------- #

###
# prototype::
#     text : a text
#     part : a part of the text we don't want surrounded by spaces.
#
#     :return: the text stripped after cleaning up the spaces around
#              the ''part'' text.
#
#
# Here is a terminal session.
#
# pyterm::
#     > from aboutmeta.tool.misc import no_space_around
#     > no_space_around("A -B  -  C  D-   G", "-")
#     'A-B-C  D-G'
#     > no_space_around(" -  ABC   - ", "-")
#     '-ABC-'
#     > no_space_around("  A   B    C  ", " ")
#     'A B C'
#     > no_space_around("", " ")
#     ''
###
def no_space_around(
    text: str,
    part: str
) -> str:
    text = [
        p.strip()
        for p in text.split(part)
        if p
    ]

    text = part.join(text)

    return text


###
# prototype::
#     text : a text
#
#     :return: the text stripped with multiple consecutive spaces
#              replaced by single spaces.
#
#     :see: no_space_around
#
#
# Here is a terminal session.
#
# pyterm::
#     > from aboutmeta.tool.misc import single_spaces
#     > single_spaces("A   B    C")
#     'A B C'
#     > single_spaces("   A   B    C   ")
#     'A B C'
#     > single_spaces("")
#     ''
###
def single_spaces(text: str) -> str:
    return no_space_around(text, " ")


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    print()
    print("## no_space_around ##")

    for txt, part in [
        ("A -B  -  C  D-   G", "-"),
        (" -  ABC   - ", "-"),
        ("  A   B    C  ", " "),
        ("", " "),
    ]:
        print()
        print(f'{txt                        = }')
        print(f'{part                       = }')
        print(f'{no_space_around(txt, part) = }')


    print()
    print("## single_spaces ##")

    for txt in [
        "A   B    C",
        "   A   B    C   ",
        '',
    ]:
        print()
        print(f'{txt                = }')
        print(f'{single_spaces(txt) = }')
