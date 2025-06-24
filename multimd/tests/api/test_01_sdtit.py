#!/usr/bin/env python3

from multimd import stdit, Path

THIS_DIR = Path(__file__).parent

DATA_OK_DIR = THIS_DIR.parent / "data" / "OK" / "stdit"
TEMP_OK_DIR = DATA_OK_DIR / ".temp"

if not TEMP_OK_DIR.is_dir():
    TEMP_OK_DIR.mkdir()

def test_stdit_OK():
    allfiles = [f for f in DATA_OK_DIR.glob("*/INIT.md")]
    allfiles.sort()

    for init_MD in allfiles:
        src       = init_MD
        src_dir   = init_MD.parent
        test_name = src_dir.name
        dest      = TEMP_OK_DIR / f"{test_name}.md"
        wanted    = src_dir / "WANTED.md"

        stdit(src, dest, True)

        lines_build  = dest.read_text(encoding = "utf8").split('\n')
        lines_wanted = wanted.read_text(encoding = "utf8").split('\n')

        assert lines_build == lines_wanted, f"see ''{test_name}.md''"
