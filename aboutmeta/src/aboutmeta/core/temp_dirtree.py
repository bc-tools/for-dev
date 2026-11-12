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
#     dirview : dirview using \yaml syntax (see below).
#
#     :action: creation of a temporary folder containing dummy
#              files and folders that follow the dirview \spec.
#              The temporary folder is deleted upon exiting the
#              context manager invoked via the instrutcion
#              ''with temp_dirtree(dirview) as d: ...''.
#
#     :yield: path of the temporary folder.
#
#
# Here is an example of what a possible ''dirview'' looks like.
#
# yaml::
#     - file-1.txt
#     - file-2.txt
#     - folder-1:
#       - README.md
#       - src:
#         - main.py
#         - CLI.py
#     - folder-2:
#       - TODO.txt
###
@contextmanager
def temp_dirtree(dirview: str) -> Path:
    py_dirview = safe_load(dirview)

    with tempfile.TemporaryDirectory() as tmpdir:
        tempdir  = Path(tmpdir)
        prepaths = []

###
# prototype::
#     name : name of a file or a folder.
#
#     :return: path built by combining ''tempdir'' (which is
#              defined above) with the path segments stored
#              in ''prepaths'', followed by ''name''.
###
        def fullpath(name: str) -> Path:
            full_path = tempdir

            for ppath in prepaths:
                full_path /= ppath

            full_path /= name

            return full_path

###
# prototype::
#     py_dirview : one dirview.
#
#     :action: add files or folders specified while iterating
#              over the current list, making recursive calls
#              to handle folder contents (which are specified
#              using a single-key dictionary).
###
        def recu_build_dirtree(py_dirview: DirTree) -> None:
            for content in py_dirview:
                if type(content) == str:
                    fullpath(content).touch()

                else:
                    for folder, subcontent in content.items():
                        fullpath(folder).mkdir()

                        prepaths.append(folder)
                        recu_build_dirtree(subcontent)
                        prepaths.pop(-1)

# It's time to work...
        recu_build_dirtree(py_dirview)

# We must return a resolved path!
        yield tempdir.resolve()


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    mydirview = """
- readme.md
- script-10.py
- script-02.py
- library:
  - main.py
  - core:
    - readme.md
    - tool.py
    """

    with temp_dirtree(mydirview) as folder:
        print(mydirview)
        print()
        print(folder)

        input('Type ENTER.')
