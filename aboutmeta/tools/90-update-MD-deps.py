#!/usr/bin/env python3

from pathlib import Path
import              re
import              subprocess


# --------------- #
# -- CONSTANTS -- #
# --------------- #

HATCH_ENV = "debug"

THIS_DIR = Path(__file__).parent
SRC_DIR  = THIS_DIR.parent
MD_DEPS_FILE  = SRC_DIR / "readme" / "deps.md"


PATTERN_NAME_VERSION = re.compile(r"([^=<>~!]+)==(.+)")

MD_HEADER = """
Complete list of dependencies
-----------------------------

Here are the `Python` libraries used by `aboutmeta`. The version numbers in brackets correspond to those used in the latest tests.
""".lstrip()

# ----------- #
# -- TOOLS -- #
# ----------- #

def get_pip_freeze_lines(src_dir, hatch_env):
    result = subprocess.run(
        [
            "hatch", "run", f"{hatch_env}:pip", "freeze"
        ],
        cwd    = src_dir,
        check  = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text   = True,
    )

    return result.stdout.splitlines()


def parse_freeze(freeze_lines):
    deps = []
    for line in freeze_lines:
# Ignore the project managed by hatch.
        if line.startswith("-e git+"):
            continue

# Extract data.
        match = PATTERN_NAME_VERSION.match(line)

        if match:
            deps.append((match.group(1), match.group(2)))

    return deps


# ----------- #
# -- TOOLS -- #
# ----------- #

content = [MD_HEADER]

freeze_lines = get_pip_freeze_lines(SRC_DIR, HATCH_ENV)

for name, version in parse_freeze(freeze_lines):
    content.append(
        f"  * `{name}`  [{version}]"
    )

content.append('')

content = "\n".join(content)

MD_DEPS_FILE.write_text(content)
