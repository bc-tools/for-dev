# ------------- #
# -- IMPORTS -- #
# ------------- #

from pathlib import Path


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     parent      : the parent folder of the path::''about.yaml''
#                   file containing the data ''content''.
#     content     : a string path of an existing file or folder.
#     auto_suffix : a suffix automatically added at the end of file
#                   paths.
#
#     :return: an instance of the class ''pathlib.Path'' giving
#              the absolute path (a relative one will be too boring
#              to use).
###
def parser(
    parent : Path,
    content    : str,
    auto_suffix: str = ""
) -> Path:
###
# Internal function factorizing the raising of errors.
###
    def raisethis(kind):
        raise ValueError(
            f"""
{kind}.
  + Data: {content}
  + Absolute path:
    {abspath}
            """.strip()
        )

# Let's work a little.
    is_dir = bool(content[-1] == "/")

# Auto-added suffixes are only for files.
    if not is_dir:
        content += auto_suffix

# Absolute path is useful.
    abspath = parent / Path(content)
    abspath = abspath.resolve()

# Does the path point to somewhere?
    if is_dir and not abspath.is_dir():
        raisethis("inexistant folder.")

    if not is_dir and not abspath.is_file():
        raisethis("inexistant file.")

# Everything looks good.
    return abspath
