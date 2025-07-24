#!/usr/bin/env python3

from typing import Tuple


# -------------------------------------- #
# -- DATA FRAMED AT THE END OF A TEXT -- #
# -------------------------------------- #

###
# prototype::
#     content : text that may or may not end with specific data
#               to be extracted, framed by the texts ''opener''
#               and ''closer''.
#     opener  : text opening the frame of data to be extracted.
#     closer  : text closing the frame of data to be extracted.
#     context : context of use (this data is only used in case
#               of error).
#
#     :return: a pair of variables ''(before, inside)'' used to
#              retrieve what precedes the data to be extracted,
#              and either ''None'' if no data has been extracted,
#              or the stripped extracted text.
#
#
# For example, we should have the following terminal session.
#
# pyterm::
#     > from aboutmeta.tool.group import extract_group
#     > extract_group("Nothing to extract", "[", "]", "DEMO_1")
#     ('Nothing to extract', None)
#     > extract_group("We have [  data ]", "[", "]", "DEMO_2")
#     ('We have', 'data')
#     > extract_group("Problem [here!", "[", "]", "DEMO_3")
#     Traceback (most recent call last):
#       ...
#         raise ValueError(
#     ValueError: missing closing '']'' for DEMO_3
###
def extract_group(
    content: str,
    opener : str,
    closer : str,
    context: str
) -> Tuple[str, str | None]:
# An opening character without its closing friend?
    if (
        not closer in content
        and
        opener in content
    ):
        raise ValueError(
            f"missing closing ''{closer}'' for {context}"
        )

# No extra data used.
    elif content[-1] != closer:
        before = content
        inside = None

# Almost done, but not totally...
    else:
# A closing character without its opening friend?
        if not opener in content:
            raise ValueError(
                f"missing opening ''{opener}'' for {context}"
            )

# All crew members are on board.
        start = content.rindex(opener)

        inside = content[start + 1 : -1].strip()
        before = content[:start].rstrip()

# Mission accomplished.
    return before, inside
