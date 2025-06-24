#!/usr/bin/env python3

from multimd import Builder, Path

THIS_DIR = Path(__file__).parent

DATA_OK_DIR = THIS_DIR.parent / "data" / "OK" / "buildit"
TEMP_OK_DIR = DATA_OK_DIR / ".temp"

if not TEMP_OK_DIR.is_dir():
    TEMP_OK_DIR.mkdir()

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

        text_build  = dest.read_text().rstrip()
        text_wanted = final_MD.read_text().rstrip()

        assert text_build == text_wanted, f"see ''{final_MD.name}''"
