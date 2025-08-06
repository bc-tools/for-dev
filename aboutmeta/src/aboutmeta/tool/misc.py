#!/usr/bin/env python3


# -------------------------- #
# -- TRANSFORMING STRINGS -- #
# -------------------------- #

###
# prototype::
#     text : a text
#     part : a part of the text we don't want surrounded by spaces.
#
#     :return: the text after cleaning up the spaces around the
#             ''part'' text.
#
#
# Here is a terminal session.
#
# pyterm::
#     > from aboutmeta.tool.misc import no_space_around
#     > no_space_around("A -B  -  C-   G", "-")
#     'A-B-C-G'
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
    content = [
        p.strip()
        for p in content.split(part)
        if p
    ]

    content = part.join(content)

    return content


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
    return no_space_around(content, " ")
