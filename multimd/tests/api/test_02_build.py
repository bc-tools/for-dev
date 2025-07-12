#!/usr/bin/env python3

from multimd       import Builder, Path
from multimd.build import HTML_COMMENT_REF_2_MULTIMD


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent

DATA_OK_DIR = THIS_DIR.parent / "data" / "OK" / "buildit"
TEMP_OK_DIR = DATA_OK_DIR / ".temp"

if not TEMP_OK_DIR.is_dir():
    TEMP_OK_DIR.mkdir()


# ----------- #
# -- LEGAL -- #
# ----------- #

def test_builder_OK():
    allfiles = [f for f in DATA_OK_DIR.glob("*.md")]
    allfiles.sort()

    for final_MD in allfiles:
        src   = DATA_OK_DIR / final_MD.stem
        dest  = TEMP_OK_DIR / final_MD.name

        Builder(
            src   = src,
            dest  = dest,
            erase = True,
        ).build()

        lines_build = dest.read_text(encoding = "utf8").split('\n')

        lines_wanted = final_MD.read_text(encoding = "utf8")
        lines_wanted = HTML_COMMENT_REF_2_MULTIMD + lines_wanted
        lines_wanted = lines_wanted.split('\n')

        assert lines_build == lines_wanted, f"see ''{final_MD.name}''"
