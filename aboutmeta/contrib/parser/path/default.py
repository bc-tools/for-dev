#!/usr/bin/env python3

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
def parser(yaml_file_dir: Path, content: str) -> Path:
    return repr(yaml_file_dir)
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


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent

# Working examples.
    for onepath in [
        str(Path(__file__).relative_to(THIS_DIR)),
        f"{THIS_DIR.relative_to(THIS_DIR)}/",
    ]:
        print()
        print(f'--- {onepath}')

        path_data = parser(THIS_DIR, onepath)

        print(f"   --> {repr(path_data)}")

    print()

# Corrupted data.
    onepath = f"{__file__}XXX"
    onepath = f"{__file__}/"

    print(f'--- CORRUPTED: {onepath}')

    path_data = parser(THIS_DIR, onepath)
