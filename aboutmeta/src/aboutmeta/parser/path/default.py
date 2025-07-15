# ------------- #
# -- IMPORTS -- #
# ------------- #

from pathlib import Path


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : a string path of an existing file or folder.
#
#     :return: an instance of the class ''pathlib.Path'' giving
#              the absolute path, and not only a relative one.
###
def parser(content: str) -> Path:
    p = Path(content)

    isdir = bool(content[-1] == "/")

    if isdir and not p.is_dir():
        raise ValueError(
             "inexistant folder.\n"
            f"  + Data: {content}\n"
            f"  + Path:{p}"
        )

    if not isdir and not p.is_file():
        raise ValueError(
             "inexistant file.\n"
            f"  + Data: {content}\n"
            f"  + Path: {p}"
        )

    return (isdir, p)