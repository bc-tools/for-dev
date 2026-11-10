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

CONTEXT  = 'data'
MSG_CTXT = f'{CONTEXT} class contrib'


THIS_DIR    = Path(__file__).parent
PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'aboutmeta'):
    PROJECT_DIR = PROJECT_DIR.parent

TESTS_DIR   = PROJECT_DIR / 'tests' / 'api' / CONTEXT / 'contribs'
CONTRIB_DIR = PROJECT_DIR / 'contribute' / 'api' / CONTEXT


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


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

add_missing_dir(TESTS_DIR)
empty_dir(TESTS_DIR)


for folder, contribs in get_accepted_paths(
    context     = CONTEXT,
    contrib_dir = CONTRIB_DIR
).items():
    ctxt = folder.parent.name

    logging.info(f"Working on '{ctxt}' codes.")

    for one_contrib in sorted(contribs):
# Extract the tests from the contribution.
        contrib_file = folder / one_contrib

        code_for_tests = hd_split_pyfile(contrib_file)[SECTION_TESTS]

        for q in "'\"":
            code_for_tests = code_for_tests.replace(
                f'if __name__ == {q}__main__{q}:',
                ''
            )

        for p in [
            PATTERN_DEV_SECTION,
            PATTERN_TEST_FUNC,
        ]:
            code_for_tests = p.sub('', code_for_tests)

        code_for_tests = PATTERN_TEST_TITLE.sub(final_comment_title, code_for_tests)

        code_for_tests = PATTERN_ONE_INDENT.sub(
            '',
            code_for_tests
        )

        code_for_tests = f'{SHEBANG_PYTHON}\n{code_for_tests}'

# Add the original source used.
        code_for_tests = add_pysrc_used(
            code     = code_for_tests,
            path_src = contrib_file.relative_to(PROJECT_DIR.parent)
        )

# We can create / update the source file.
        create_update_file(
            file    = TESTS_DIR / f'test_{one_contrib}',
            content = code_for_tests,
        )
