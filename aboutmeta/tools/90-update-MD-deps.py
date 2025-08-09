#!/usr/bin/env python3

from utilities.common import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent
SRC_DIR  = THIS_DIR.parent

TOML_PYPROJ_FILE = SRC_DIR / "pyproject.toml"
MD_DEPS_FILE     = SRC_DIR / "readme" / "deps.md"


PATTERN_NAME_VERSION = re.compile(r"([^=<>~!]+)>=(.+)")

MD_HEADER = """
Complete list of dependencies
-----------------------------

Here are the `Python` libraries used by `aboutmeta`. The version numbers in brackets are those used prior to the release of this version of `aboutmeta`.
""".lstrip()


# --------------- #
# -- LET'S GO! -- #
# --------------- #

logging.info(f"Update ''{MD_DEPS_FILE.relative_to(SRC_DIR)}''.")

with TOML_PYPROJ_FILE.open("rb") as f:
    data = tomli.load(f)

deps = data.get("project", {}).get("dependencies", [])

content = [MD_HEADER]

for dep in deps:
    match = PATTERN_NAME_VERSION.match(dep)

    if match is None:
        raise ValueError("BUG!")

    name  = match.group(1)
    nbver = match.group(2)

    content.append(f"  * `{name}`   **[{nbver}]**")

content.append('')
content = "\n".join(content)

MD_DEPS_FILE.touch()
MD_DEPS_FILE.write_text(content)
