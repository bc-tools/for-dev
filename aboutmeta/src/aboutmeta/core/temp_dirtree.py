#!/usr/bin/env python3

from pathlib    import Path
import                 tempfile
from contextlib import contextmanager
from yaml       import safe_load


# ------------------------ #
# -- TEMPORARY DIR TREE -- #
# ------------------------ #

type DirTree = list[str | dict[str, DirTree]]

###
# prototype::
#     dirview : XXXXX
#
#     :yield: XXXXX
###
@contextmanager
def temp_dirtree(dirview: str) -> Path:
    dirtree = safe_load(dirview)

    with tempfile.TemporaryDirectory() as tmpdir:
        rootdir  = Path(tmpdir)
        prepaths = []

###
# prototype::
#     name : XXXXX
#
#     :return: XXXXX
###
        def fullpath(name: str) -> Path:
            full_path = rootdir

            for ppath in prepaths:
                full_path /= ppath

            full_path /= name

            return full_path

###
# prototype::
#     dirtree : XXXXX
#
#     :action: XXXXX
###
        def recu_build_dirtree(dirtree: DirTree) -> None:
            for content in dirtree:
                if type(content) == str:
                    fullpath(content).touch()

                else:
                    for folder, subcontent in content.items():
                        fullpath(folder).mkdir()

                        prepaths.append(folder)
                        recu_build_dirtree(subcontent)
                        prepaths.pop(-1)

        recu_build_dirtree(dirtree)

# We must resolve the path!!!!
        yield rootdir.resolve()


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    ...
