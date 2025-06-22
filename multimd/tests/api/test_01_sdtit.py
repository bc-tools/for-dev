#!/usr/bin/env python3

from multimd import stdit, Path

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR.parent / "data" / "stdit"
TEMP_DIR = DATA_DIR / ".temp"

if not TEMP_DIR.is_dir():
    TEMP_DIR.mkdir()

def test_stdit():
    for init_MD in DATA_DIR.glob("*/INIT.md"):
        src       = init_MD
        src_dir   = init_MD.parent
        test_name = src_dir.name
        dest      = TEMP_DIR / f"{test_name}-{src.name}"
        wanted    = src_dir / "WANTED.md"

        stdit(src, dest, True)

        text_build  = dest.read_text()
        text_wanted = wanted.read_text()

        assert text_build == test_name, f"see ''{test_name}.md''"
