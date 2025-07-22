# ------------- #
# -- IMPORTS -- #
# ------------- #

from typing import List

from pathlib import Path
import              re

from natsort import natsorted

from aboutmeta.data import constants, tocpath


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     parent : the parent directory of the path::''about.yaml’' file
#              from which the ''data’' \arg comes.
#     data   : a virtual path that is either a relative path in the
#              form of a string, a \glob or \regex pattern with the
#              patterns provided using a single-key \dict.
#
#     :return: an instance of the class ''tocpath.TOCPath'' to work
#              easily with the ''toc'' path: initial data, kind and
#              absolute paths build.
#
#
# Let's look at some virtual examples where we assume that the parent
# folder has the absolute path path::“”/abs/path/readme''.
#
#
# [[An existing file]]
#
# Let's assume that the file path ::''/abs/path/readme/api.md'' exists.
# In this case, using ''data = "api.md"'' will imply the return of the
# following ''tocpath.TOCPath''. The use of a list can be understood
# by looking at the paths returned when using \glob or \regex patterns
# (see below).
#
# python::
#     TOCPath(
#         data  = 'api/md',
#         kind  = 'files',
#         paths = [PosixPath('/abs/path/readme/api.md')]})
#
#
# [[An existing folder]]
#
# Let's assume that the folder path ::''/abs/path/readme/api'' exists.
# In this case, using ''data = "api/"'' will imply the return of the
# following ''tocpath.TOCPath'' indicating that the yaml::''toc''
# block of an path::''about.yaml'' file need to be analyzed.
#
# python::
#     TOCPath(
#         data  = 'api/',
#         kind  = 'about',
#         paths = PosixPath('/abs/path/readme/api/about.yaml')})
#
#
# [[A \glob pattern]]
#
# If ''data = {'glob': "*.md"}'' is used, and the \glob pattern finds
# paths, then something like the following ''tocpath.TOCPath'' can be
# returned, the list being sorted "naturally" via ''natsort'' module.
#
# python::
#     TOCPath(
#         data  = {'glob': '*.md'},
#         kind  = 'files',
#         paths = [PosixPath('/abs/path/readme/about.md'),
#                  PosixPath('/abs/path/readme/api.md'),
#                  PosixPath('/abs/path/readme/specs.md')]})
#
#
# [[A "flat" \regex pattern]]
#
# If ''data = {'regex': r".*\.md"}'' is used, and the \regex
# pattern finds paths directly in the parent folder, then something
# like the following ''tocpath.TOCPath'' can be returned, the list
# being sorted "naturally" via the ''natsort'' module.
#
# python::
#     TOCPath(
#         data  = {'regex': '.*\\.md'},
#         kind  = 'files',
#         paths = [PosixPath('/abs/path/readme/about.md'),
#                  PosixPath('/abs/path/readme/api.md'),
#                  PosixPath('/abs/path/readme/deps.md')]})
#
#
# [[A "recursive" \regex pattern]]
#
# If ''data = {'recreg': r".*\.md"}'' is used, and the \regex
# pattern finds paths recursively in the parent folder, then something
# like the following ''tocpath.TOCPath'' can be returned, the list
# being sorted "naturally" via the ''natsort'' module. Note that here
# subfolders have been analyzed recursively.
#
# python::
#     TOCPath(
#         data  = {'recreg': '.*\\.md'},
#         kind  = 'files',
#         paths = [PosixPath('/abs/path/readme/about.md'),
#                  PosixPath('/abs/path/readme/api.md'),
#                  PosixPath('/abs/path/readme/api/extract.md'),
#                  PosixPath('/abs/path/readme/api/use.md'),
#                  PosixPath('/abs/path/readme/api/use/project.md'),
#                  PosixPath('/abs/path/readme/api/use/toc.md'),
#                  PosixPath('/abs/path/readme/api/validate.md'),
#                  PosixPath('/abs/path/readme/api/validate/email.md'),
#                  PosixPath('/abs/path/readme/api/validate/url.md'),
#                  PosixPath('/abs/path/readme/deps.md')]}
###
def parser(
    parent: Path,
    data  : str | dict
) -> tocpath.TOCPath:
###
# Internal function to raise errors.
###
    def _raisethis(
        kind: str,
        xtra: str = ""
    ) -> None:
        raise ValueError(
            f"""
{kind}.
    + Data  : {data!r}
    + Parent: {parent}
{xtra}
            """.strip()
        )

# "Direct" path.
    if isinstance(data, str):
        is_dir = bool(data[-1] == "/")

# Absolute path is useful.
        abspath = parent / Path(data)
        abspath = abspath.resolve()

# File?
        if not is_dir:
            if not abspath.is_file():
                _raisethis("inexistant file")

            kind    = constants.TAG_TOC_PATH_FILES
            abspath = [abspath]

# Folder?
        else:
            if not abspath.is_dir():
                _raisethis("inexistant folder")

            sub_yaml_file = abspath / "about.yaml"

            if not sub_yaml_file.is_file():
                _raisethis("missing sub ''about.yaml'' file")

            kind    = constants.TAG_TOC_PATH_ABOUT
            abspath = sub_yaml_file

# "Direct" path looks good.
        return tocpath.TOCPath(
            data  = data,
            kind  = kind,
            paths = abspath
        )

# Pattern needs a one-key dict!
    if not isinstance(data, dict):
        _raisethis("one dict expected for one glob or regex pattern")

    if not len(data.keys()) == 1:
        _raisethis("one single key expected for a pattern dict")

    for kind, pattern in data.items():
        ...

    if not kind in constants.TAG_TOC_PATTERN_KINDS:
        _raisethis(f"illegal pattern kind ''{kind}''")

# ''glob'' pattern.
    if kind == constants.TAG_TOC_PATH_GLOB:
        all_abspaths = [
            p
            for p in parent.glob(pattern)
            if p.is_file()
        ]

# ''regex'' pattern.
    else:
        try:
            pattern = re.compile(pattern)

        except re.error as e:
            _raisethis(
                kind = f"regex compilation failed for {pattern!r}",
                xtra = f"REGEX ERROR: {e}"
            )

        all_abspaths = []

        _glob = "glob" if kind == "regex" else "rglob"

        for fullpath in getattr(parent, _glob)("*"):
            relpath = fullpath.relative_to(parent)

            if pattern.fullmatch(str(relpath)):
                all_abspaths.append(fullpath)

# Winning pattern?
    if not all_abspaths:
        _raisethis(f"no files found with the pattern")

    return tocpath.TOCPath(
        data  = data,
        kind  = constants.TAG_TOC_PATH_FILES,
        paths = natsorted(all_abspaths)
    )
