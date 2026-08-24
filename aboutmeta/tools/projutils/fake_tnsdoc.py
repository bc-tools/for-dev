#!/usr/bin/env python3

from .constants import *


# -------------------- #
# -- YYY -- #
# -------------------- #

def comment_2_tnsdoc(comment):
    lines = []

    for l in comment.splitlines():
        if l == MAGIC_COMMENT_DELIM:
            continue

        l = l[1:]

        if l and l[0] == ' ':
            l = l[1:]

        lines.append(l)

    comment = '\n'.join(lines)
    comment = comment.strip()

    return comment
