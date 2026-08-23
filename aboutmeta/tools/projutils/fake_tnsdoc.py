#!/usr/bin/env python3


# -------------------- #
# -- YYY -- #
# -------------------- #

def comment_2_tnsdoc(comment):
    lines = [
        l[2:].rstrip()
        for l in comment.splitlines()
        if l and (
            l.rstrip() == '#'
            or
            l[:2] == '# '
        )
    ]

    comment = '\n'.join(lines)
    comment = comment.strip() + '\n'

    return comment
