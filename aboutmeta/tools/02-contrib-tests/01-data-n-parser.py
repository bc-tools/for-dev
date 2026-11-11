#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.logconf    import *
from cbutils.split_file import *
from cbutils.coding_py  import *
from cbutils.contrib    import *
from cbutils.pathplus   import *

import re

from textwrap import dedent


# ------------------ #
# -- CONSTANTS #1 -- #
# ------------------ #

THIS_DIR    = Path(__file__).parent
PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'aboutmeta'):
    PROJECT_DIR = PROJECT_DIR.parent


# ------------------ #
# -- CONSTANTS #2 -- #
# ------------------ #

SECTION_TESTS = 'TESTS'

PATTERN_DEV_SECTION = re.compile(
    r'^# dev:.*?\n.*?[ \t]*# :dev\s*$',
    flags = re.DOTALL | re.MULTILINE
)

PATTERN_TEST_FUNC = re.compile(
    r"^[^\S\r\n]*(test_\w+)\(\)\s*$",
    flags = re.MULTILINE
)


def final_comment_title(match):
    title  = match.group(2)

    inner  = f"# -- {title} -- #"
    border = "# " + "-" * (len(inner) - 4) + " #"

    return f"""


    {border}
    {inner}
    {border}
    """.rstrip() + '\n'

PATTERN_TEST_TITLE = re.compile(
    r"(?:[^\S\r\n]*\r?\n)*([^\S\r\n]*)#\s*--\s*(.+?)\s*--\s*#"
)


PATTERN_ONE_INDENT = re.compile(
    r"^[ ]{1,4}",
    flags = re.MULTILINE
)


# ----------- #
# -- TOOLS -- #
# ----------- #

POSSIBLE_TRIPLE_QUOTES = [
    q*3
    for q in '"\''
]

def remove_indents(code):
    newlines = []
    in_multiline_str   = False
    last_triple_quotes = None

    for line in code.split('\n'):
# Line to copy verbatim.
        if in_multiline_str:
            newlines.append(line)

# Closing a multiline content.
            if line.endswith(last_triple_quotes):
                in_multiline_str = False

            continue

# Line to analyze.
        line = line.rstrip()

# Empty line.
        if not line:
            newlines.append('')
            continue

# Must be a line-start comment.
        if line.lstrip() == line:
            newlines.append(line)
            continue

# Line to dedent.
        shift = (
            1
            if line.startswith('\t') else
            4
        )

        newlines.append(line[shift:])

# Opening a multiline content.
        for tq in POSSIBLE_TRIPLE_QUOTES:
            if line.endswith(tq):
                in_multiline_str   = True
                last_triple_quotes = tq

                break

# Nothing left to do.
    return '\n'.join(newlines)


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

for nb_ctxt, ctxt in enumerate(
    [
        'data',
        'parser',
    ],
    start = 1,
):
    msg_ctxt = f'{ctxt} contrib tests'

    tests_dir   = PROJECT_DIR / 'tests' / 'api' / f'{nb_ctxt:02}-{ctxt}' / 'contribs'
    contrib_dir = PROJECT_DIR / 'contribute' / 'api' / ctxt


    for folder, contribs in get_accepted_paths(
        context     = ctxt,
        contrib_dir = contrib_dir
    ).items():
        ctxt = folder.parent.name

        logging.info(f"Working on '{ctxt}' tests.")

        for _ in [
            add_missing_dir,
            empty_dir,
        ]:
            _(tests_dir)

        for one_contrib in sorted(contribs):
            contrib_name = Path(one_contrib).stem

# Extract the tests from the contribution.
            contrib_file = folder / one_contrib

            code = hd_split_pyfile(contrib_file)[SECTION_TESTS]

            for q in "'\"":
                code = code.replace(
                    f'if __name__ == {q}__main__{q}:',
                    ''
                )

            for p in [
                PATTERN_DEV_SECTION,
                PATTERN_TEST_FUNC,
            ]:
                code = p.sub('', code)

            code = PATTERN_TEST_TITLE.sub(final_comment_title, code)
            code = remove_indents(code)
            code = code.strip()
            code = f'{SHEBANG_PYTHON}\n{code}'

# Add the original source used.
            code = add_pysrc_used(
                code     = code,
                path_src = contrib_file.relative_to(PROJECT_DIR.parent)
            )

# Add the aboutmeta import.
            code = code.replace(
                SHEBANG_PYTHON,
                f'''
{SHEBANG_PYTHON}

# Needed extra imports.

from aboutmeta.core.errors import *
from aboutmeta.specs.{ctxt}.{contrib_name} import *
                '''.strip()
            )

# We can create / update the source file.
            create_update_file(
                file    = tests_dir / f'test_{ctxt}_contrib_{one_contrib}',
                content = code,
            )
