#!/usr/bin/env python3

from multimd import Builder, Path

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR.parent / "data" / "buildit"
TEMP_DIR = DATA_DIR / ".temp"

def test_std_md():
    for final_MD in DATA_DIR.glob("*.md"):
        src   = DATA_DIR / final_MD.stem
        dest  = TEMP_DIR / final_MD.name

        Builder(
            src   = src,
            dest  = dest,
            erase = True,
        ).build()

        text_build    = dest.read_text().rstrip()
        text_expected = final_MD.read_text().rstrip()

        assert text_build == text_expected
