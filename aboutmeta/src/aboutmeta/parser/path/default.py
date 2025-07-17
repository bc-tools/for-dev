# ------------- #
# -- IMPORTS -- #
# ------------- #

from pathlib import Path


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     parent_dir : XXXX
#     content    : a string path of an existing file or folder.
#
#     :return: an instance of the class ''pathlib.Path'' giving
#              the absolute path, and not only a relative one.
###
def parser(
    parent_dir : Path,
    content    : str,
    auto_suffix: str = ""
) -> Path:
    isdir = bool(content[-1] == "/")

    if not isdir:
        content += auto_suffix

    abspath = parent_dir / Path(content)
    abspath = abspath.resolve()

    if isdir and not abspath.is_dir():
        raise ValueError(
             "inexistant folder.\n"
            f"  + Data: {content}\n"
            f"  + Path: {abspath}"
        )

    if not isdir and not abspath.is_file():
        raise ValueError(
             "inexistant file.\n"
            f"  + Data: {content}\n"
            f"  + Path: {abspath}"
        )

    return (isdir, abspath)