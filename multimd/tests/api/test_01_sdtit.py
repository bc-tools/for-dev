#!/usr/bin/env python3

from multimd import stdit, Path

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR.parent / "data" / "stdit"
TEMP_DIR = DATA_DIR / ".temp"

def test_stdit():
    for init_MD in DATA_DIR.glob("*/INIT.md"):
        src     = init_MD
        src_dir = init_MD.parent
        dest    = TEMP_DIR / f"{src_dir.name}-{src.name}"
        wanted  = src_dir / "WANTED.md"

        print('')
        print(src)
        print(dest)
        print(wanted)

        # Builder(
        #     src   = src,
        #     dest  = dest,
        #     erase = True,
        # ).build()

        # text_build    = dest.read_text().rstrip()
        # text_expected = final_MD.read_text().rstrip()

        # assert text_build == text_expected


test_stdit()
