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
#     :return: XXXXX
#              an instance of the class ''pathlib.Path'' giving
#              the absolute path, and not only a relative one.
###
def parser(
    parent_dir : Path,
    content    : str,
    auto_suffix: str = ""
) -> Path:
    def raisethis(kind):
        raise ValueError(
            f"{kind}.\n"
            f"  + Data: {content}\n"
            f"  + Path: {abspath}"
        )


    isdir = bool(content[-1] == "/")

    if not isdir:
        content += auto_suffix

    abspath = parent_dir / Path(content)
    abspath = abspath.resolve()

    if isdir and not abspath.is_dir():
        raisethis("inexistant folder.")

    if not isdir and not abspath.is_file():
        raisethis("inexistant file.")

    return (isdir, abspath)
