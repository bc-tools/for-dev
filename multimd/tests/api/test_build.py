#!/usr/bin/env python3

from multimd import Builder, Path

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR.parent / "data"

for final_MD in DATA_DIR.glob("*.md"):
    print(final_MD.stem)

def test_builder():
    ...

    # Builder(
    #     src   = THIS_DIR / f'build-{kind}',
    #     dest  = THIS_DIR / f'build-{kind}-final.md',
    #     erase = True,
    # ).build()
