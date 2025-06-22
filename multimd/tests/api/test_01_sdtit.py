#!/usr/bin/env python3

from multimd import stdit, Path

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR.parent / "data" / "stdit"
TEMP_DIR = DATA_DIR / ".temp"

if not TEMP_DIR.is_dir():
    TEMP_DIR.mkdir()

def test_stdit():
    allfiles = [f for f in DATA_DIR.glob("*/INIT.md")]
    allfiles.sort()

    for init_MD in allfiles:
        src       = init_MD
        src_dir   = init_MD.parent
        test_name = src_dir.name
        dest      = TEMP_DIR / f"{test_name}.md"
        wanted    = src_dir / "WANTED.md"

        stdit(src, dest, True)

        lines_build  = dest.read_text(encoding = "utf8").split('\n')
        lines_wanted = wanted.read_text(encoding = "utf8").split('\n')

        assert lines_build == lines_wanted, f"see ''{test_name}.md''"
