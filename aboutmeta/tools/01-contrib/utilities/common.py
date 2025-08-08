#!/usr/bin/env python3

# from pprint import pprint

from pathlib     import Path
import                  re

from yaml import safe_load


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAB_1 = ' '*2
TAB_2 = TAB_1*2
TAB_3 = TAB_1*3

ITEM_1 = '+'
ITEM_2 = f'{TAB_1}*'
ITEM_3 = f'{TAB_2}-'
ITEM_4 = f'{TAB_3}-->'


INIT_FILE    = "__init__.py"
INIT_CONTENT = "#!/usr/bin/env python3\n"


TAG_STATUS = "status"
TAG_OK     = "ok"


# ----------- #
# -- PATHS -- #
# ----------- #

def get_folders(
    this_dir,
    contrib_dir,
    context,
    nbtest,
    subfolder = "code",
):
    projdir  = this_dir.parent.parent
    projname = projdir.name

    contribdir = projdir / "contrib" / contrib_dir / subfolder
    statusdir  = contribdir.parent / "status"
    srcdir     = projdir / "src" / projname / context
    testsdir   = projdir / "tests" / f"{nbtest}-{context}"

    return (
        projdir,
        projname,
        contribdir,
        statusdir,
        srcdir,
        testsdir
    )


# WARNING!
# "No status" ==> "No parser to add"
def get_accepted_paths(
    contribdir,
    statusdir,
    subfolder = "",
    ext       = 'py',
):
    files = []

    if subfolder:
        subfolder += "/"

    for yaml_file in statusdir.glob(
        f"{subfolder}*.yaml"
    ):
        statusdata = safe_load(yaml_file.read_text())

        if statusdata[TAG_STATUS] != TAG_OK:
            continue

        file = contribdir / f"{yaml_file.stem}.{ext}"

        if not file.is_file():
            raise IOError(f"missing file:\n{file}")

        files.append(file)

    files.sort()

    return files
