#!/usr/bin/env python3

from aboutmeta.core.errors import ParsingError


# -------------------------------------- #
# -- DATA FRAMED AT THE END OF A TEXT -- #
# -------------------------------------- #

###
# prototype::
#     content   : text with, or without, a specific extremal data
#                 surrounded by the delimiters defined using the
#                 ''delims'' argument.
#     delims    : a 2-character text indicating the opening and
#                 closing characters used to frame special data.
#     context   : context of use (this text is for error messages).
#     left_most : if the value is ''True'', the "framed" data must
#                 be at the end of the text, otherwise it must be
#                 at the beginning (no data can be inside the text).
#
#     :return: a pair of variables ''(remaining, data)'' where
#              ''remaining'' is the text obtained after removing
#              the "framed" data. ''data'' is ''None'' if no data
#              has been extracted, and all constructed texts are
#              stripped.
#
#
# Here is a terminal session without any error.
#
# pyterm::
#     > from aboutmeta.tool.group import extract_group
#     > extract_group("Nothing to extract", "[]", "OK_1")
#     ('Nothing to extract', None)
#     > extract_group("We have [  data ]", "[]", "OK_2")
#     ('We have', 'data')
#     > extract_group("[Data] before me!", "[]", "OK_3", False)
#     ('before me!', 'Data')
#
#
# Here is a terminal session with errors.
#
# pyterm::
#     > from aboutmeta.tool.group import extract_group
#     > extract_group("Not opened!]", "[]", "KO_1")
#     Traceback (most recent call last):
#       ...
#         raise ValueError(
#     aboutmeta.core.errors.ParsingError: missing opening ''['' for KO_1.
#     > extract_group("Not [closed!", "[]", "KO_2")
#     Traceback (most recent call last):
#       ...
#         raise ValueError(
#     aboutmeta.core.errors.ParsingError: missing closing '']'' for KO_2.
#     > extract_group("Mis]placed[ delims", "[]", "KO_3")
#     Traceback (most recent call last):
#       ...
#         raise ValueError(
#     aboutmeta.core.errors.ParsingError: missing closing '']'' at the end for KO_3.
#     > extract_group("[Bad data] before", "[]", "KO_4")
#     Traceback (most recent call last):
#       ...
#         raise ValueError(
#    aboutmeta.core.errors.ParsingError: missing closing '']'' at the end for KO_4.
###
def extract_group(
    content  : str,
    delims   : list[str],
    context  : str,
    left_most: bool = True
) -> tuple[str, str | None]:
# Two delimiting characters?
    if len(delims) != 2:
        raise ValueError(
            "two characters needed as delimiters: ''{delims}''."
        )

    opener, closer = delims

# No delimiter used.
    if (
        not closer in content
        and
        not opener in content
    ):
        return (content, None)

# One of the delimiters is alone. Poor lonesome character...
    for missing, found, kind in [
        (closer, opener, "closing"),
        (opener, closer, "opening"),
    ]:
        if (
            not missing in content
            and
            found in content
        ):
            raise ParsingError(
                f"missing {kind} ''{missing}'' for {context}."
            )

# Good use of delimiters?
    if left_most:
        extrem_pos  = -1
        extrem_char = closer

    else:
        extrem_pos  = 0
        extrem_char = opener

    if content[extrem_pos] != extrem_char:
        if extrem_pos == 0:
            what  = "opening"
            where = "begining"

        else:
            what  = "closing"
            where = "end"

        raise ParsingError(
            f"missing {what} ''{extrem_char}'' at "
            f"the {where} for {context}."
        )

# Let's extract special data.
    if extrem_pos == 0:
        end       = content.index(closer)
        data      = content[1:end].strip()
        remaining = content[end + 1:].strip()

    else:
        start     = content.rindex(opener)
        data      = content[start + 1 : -1].strip()
        remaining = content[:start].strip()

# Mission accomplished.
    return (remaining, data)


###
# prototype::
#     groups : a list of texts to be framed.
#     delims : texts indicating "framing" characters.
#            @ len(groups) = len(delims)
#
#     :return: the text obtained by joining the framed texts with
#              spaces.
#
#
# Here is a terminal session.
#
# pyterm::
#     > from aboutmeta.tool.group import gather_groups
#     > gather_groups(
#         ["Someone", "email@test.org", "Institute, Galaxy"],
#         ["", "[]", "()"]
#     )
#     'Someone [email@test.org] (Institute, Galaxy)'
#     > gather_groups(
#         ["Someone", "email@test.org", "Institute, Galaxy"],
#         ["", "[", "()"]
#     )
#     Traceback (most recent call last):
#     ...
#         raise ValueError(
#     ValueError: two characters needed as delimiters, see '[' in delims = ['', '[', '()'].
#     > gather_groups(
#         ["Someone", "email@test.org", "Institute, Galaxy"],
#         ["[]", "()"]
#     )
#     Traceback (most recent call last):
#     ...
#         raise ValueError("groups and delims must have the same length.")
#     ValueError: lists ''groups'' and ''delims'' must have the same length.
###
def gather_groups(
    groups: list[str],
    delims: list[str],
) -> str:
# Same sizes?
    if len(groups) != len(delims):
        raise ValueError(
            "lists ''groups'' and ''delims'' must have the same length."
        )

# Let's apply the delimiters.
    content = []

    for grp, dlm in zip(groups, delims):
        if dlm != "":
# We need two delimiters.
            if len(dlm) != 2:
                raise ValueError(
                     "two characters needed as delimiters, "
                    f"see {dlm!r} in delims = {delims!r}."
                )

            l, r = dlm
            grp  = f"{l}{grp}{r}"

        content.append(grp)

# Eveything looks good.
    content = " ".join(content)

    return content
