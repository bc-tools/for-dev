#!/usr/bin/env python3

from pathlib import Path


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR    = Path(__file__).parent
CONTRIB_DIR = THIS_DIR.parent.parent / "contrib"
README_FILE = CONTRIB_DIR / "README.md"


TEMPL_TAG_STRUCT = "<!-- FOLDER STRUCT. AUTO - {} -->"

TAG_STRUCT_START = TEMPL_TAG_STRUCT.format("START")
TAG_STRUCT_END   = TEMPL_TAG_STRUCT.format("END")


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

content = README_FILE.read_text()

# Check initial content!
for tag in [
    TAG_STRUCT_START,
    TAG_STRUCT_END,
]:
    if content.count(tag) != 1:
        raise ValueError(
            f"use the following special comment only once.\n{tag}"
        )

before, _, after = content.partition(f"\n{TAG_STRUCT_START}")
_     , _, after = after.partition(f"{TAG_STRUCT_END}\n")

# The list of folders.
folders = [
    p.name
    for p in CONTRIB_DIR.glob('*')
    if p.is_dir()
]

# Content updated.
folders = '\n      + '.join(folders)

content = f"""{before.strip()}

{TAG_STRUCT_START}
    + {CONTRIB_DIR.name}
      + {folders}
{TAG_STRUCT_END}
{after.rstrip()}
"""

README_FILE.write_text(content)
