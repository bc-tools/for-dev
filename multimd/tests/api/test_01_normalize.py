#!/usr/bin/env python3

from multimd       import Builder, Path
from multimd.build import HTML_COMMENT_REF_2_MULTIMD

THIS_DIR = Path(__file__).parent

DATA_OK_DIR = THIS_DIR.parent / "data" / "OK" / "normalize"
TEMP_OK_DIR = DATA_OK_DIR / ".temp"

if not TEMP_OK_DIR.is_dir():
    TEMP_OK_DIR.mkdir()

def test_normalize_OK():
    allfiles = [f for f in DATA_OK_DIR.glob("*/alone.md")]
    allfiles.sort()

    for alone_MD in allfiles:
        src       = alone_MD.parent
        test_name = src.name
        dest      = TEMP_OK_DIR / f"{test_name}.md"
        wanted    = DATA_OK_DIR / f"{test_name}.md"

        Builder(
            src   = src,
            dest  = dest,
            erase = True,
        ).build()

        lines_build = dest.read_text(encoding = "utf8").split('\n')

        lines_wanted = wanted.read_text(encoding = "utf8")
        lines_wanted = HTML_COMMENT_REF_2_MULTIMD + lines_wanted
        lines_wanted = lines_wanted.split('\n')

        assert lines_build == lines_wanted, f"see ''{test_name}.md''"
