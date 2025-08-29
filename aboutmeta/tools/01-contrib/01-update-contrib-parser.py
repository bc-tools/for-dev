#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.core import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR    = Path(__file__).parent
PROJECT_DIR = THIS_DIR.parent.parent
CONTRIB_DIR = PROJECT_DIR / "contrib"
SRC_DIR     = PROJECT_DIR / "src" / "aboutmeta" / "specs"

PYCODE_CONTRIB_DIRS = [
    CONTRIB_DIR / "parser",
    CONTRIB_DIR / "data",
]
PYCODE_CONTRIB_DIRS = [p / "code" for p in PYCODE_CONTRIB_DIRS]


HEADERS_IGNORED = [
    (SECTION_TESTS:= "TESTS"),
    (SECTION_TOOLS:= "TOOLS"),
]


# ----------- #
# -- TOOLS -- #
# ----------- #

def get_xtra_files(file: Path) -> list[Path]:
    xtra_files = [
        p
        for p in file.parent.glob(
            f"{file.stem}-*"
        )
        if p != file
    ]

    return xtra_files


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

add_missing_init(SRC_DIR)

for folder, contribs in get_accepted_paths(PROJECT_DIR).items():
    if not folder in PYCODE_CONTRIB_DIRS:
        continue

    ctxt = folder.parent.name

    logging.info(f"Working on '{ctxt}'.")

    dest_dir = SRC_DIR / ctxt

    add_missing_dir(dest_dir)
    add_missing_init(dest_dir)

    for one_contrib in contribs:
# Adding a new Python code.
        contrib_file = folder / one_contrib

        final_code = finalize_pycode(
            file            = contrib_file,
            headers_ignored = HEADERS_IGNORED
        )

        if final_code:
            log_raise_error(
                exception = ValueError,
                context   = "contrib",
                desc      = f"Empty file validated:\n'{contrib_file}'.",
            )

        create_update_file(
            file    = dest_dir / one_contrib,
            content = final_code,
        )

# Extra files?
        xtra_files = get_xtra_files(contrib_file)

        if xtra_files:
            plurial = "s" if len(xtra_files) != 1 else ""

            logging.warning(f"Extra file{plurial} used.")

            for xfile in xtra_files:
                create_update_file(
                    file      = dest_dir / xfile.name,
                    content   = xfile.read_text() + "\n",
                    log_level = TAG_WARNING
                )
