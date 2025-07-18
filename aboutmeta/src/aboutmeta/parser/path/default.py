# ------------- #
# -- IMPORTS -- #
# ------------- #

from pathlib import Path


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     parent : XXXX
#     content    : a string path of an existing file or folder.
#
#     :return: XXXXX
#              an instance of the class ''pathlib.Path'' giving
#              the absolute path, and not only a relative one.
###
def parser(
    parent : Path,
    content    : str,
    auto_suffix: str = ""
) -> Path:
    def raisethis(kind):
        raise ValueError(
            f"""
{kind}.
  + Data: {content}
  + Absolute path:
    {abspath}
            """.strip()
        )

    is_dir = bool(content[-1] == "/")

    if not is_dir:
        content += auto_suffix

    abspath = parent / Path(content)
    abspath = abspath.resolve()

    if is_dir and not abspath.is_dir():
        raisethis("inexistant folder.")

    if not is_dir and not abspath.is_file():
        raisethis("inexistant file.")

    return abspath