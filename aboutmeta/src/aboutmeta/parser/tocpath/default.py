# ------------- #
# -- IMPORTS -- #
# ------------- #

from typing import List

from pathlib import Path
import              re

from aboutmeta.data.constants import *


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     parent : the parent directory of the path::''about.yaml’' file
#              from which the ''data’' \arg comes.
#     data   : a virtual path that is either a relative path in the
#              form of a string, a \glob pattern, or a \regex pattern,
#              with the patterns provided using a single-key \dict.
#
#     :return: XXX
###
def parser(
    parent: Path,
    data  : str | dict
) -> dict[str: Path | List[Path]]:
###
# Intrenal function to raise errors.
###
    def _raisethis(
        kind: str,
        xtra: str = ""
    ) -> None:
        raise ValueError(
            f"""
{kind}.
    + Data  : {data!r}
    + Parent: {parent}
{xtra}
            """.strip()
        )

# "Direct" path.
    if isinstance(data, str):
        is_dir = bool(data[-1] == "/")

# Absolute path is useful.
        abspath = parent / Path(data)
        abspath = abspath.resolve()

# File?
        if not is_dir:
            if not abspath.is_file():
                _raisethis("inexistant file")

            kind = TAG_TOC_PATH_FILE

# Folder?
        else:
            if not abspath.is_dir():
                _raisethis("inexistant folder")

            sub_yaml_file = abspath / "about.yaml"

            if not sub_yaml_file.is_file():
                _raisethis("missing sub ''about.yaml'' file")

            kind    = TAG_TOC_PATH_ABOUT
            abspath = sub_yaml_file

# "Direct" path looks good.
        return {kind: abspath}

# Pattern needs a one-level dict!
    if not isinstance(data, dict):
        _raisethis("one dict expecting for one glob or regex pattern")

    if not len(data.keys()) == 1:
        _raisethis("one single key expected for a pattern dict")

    for kind, pattern in data.items():
        ...

    if not kind in TAG_TOC_PATTERN_KINDS:
        _raisethis(f"illegal pattern kind ''{kind}''")

# ''glob'' pattern.
    if kind == TAG_TOC_PATH_GLOB:
        all_abspaths = [
            p
            for p in parent.glob(pattern)
            if p.is_file()
        ]

# # ''regex'' pattern.
#     else:
#         pattern = re.compile(pattern)
#         TODO_REGEX

# Winning pattern?
    if not all_abspaths:
        _raisethis(f"no files found with the pattern")

    return {kind: all_abspaths}
