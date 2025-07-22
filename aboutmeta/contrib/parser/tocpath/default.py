# ------------- #
# -- IMPORTS -- #
# ------------- #

from typing import List

from pathlib import Path
import              re

from natsort import natsorted

from aboutmeta.data import constants


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     parent : the parent directory of the path::''about.yaml’' file
#              from which the ''data’' \arg comes.
#     data   : a virtual path that is either a relative path in the
#              form of a string, a \glob pattern, or a \regex pattern,
#              with the patterns provided using a single-key \dict.
#
#     :return: a single-key \dict indicating the kind of paths build
#              associated to the paths build (using instances of the
#              ''pathlib.Path'' class).
#
#
# For our examples, we suppose that is path::''/abs/path/readme'' is
# the parent folder.
#
#
# [An existing file]
#
# Let's assume that the file path ::''/abs/path/readme/api.md'' exists.
# In this case, using ''data = "api.md"'' will imply the return of the
# following \dict. The use of a list can be understood by looking at
# the paths returned when using \glob or \regex patterns (see below).
#
# python::
#     {'files': [PosixPath('/abs/path/readme/api.md')]}
#
#
# [An existing folder]
#
# Let's assume that the folder path ::''/abs/path/readme/api'' exists.
# In this case, using ''data = "api/"'' will imply the return of the
# following \dict indicating that the yaml::''toc'' block of an
# path::''about.yaml'' file need to be analyzed.
#
# python::
#     {'about': PosixPath('/abs/path/readme/api/about.yaml')}
#
#
# [A \glob pattern]
#
# If ''data = {'glob': "*.md"}'' is used, and the \glob pattern finds
# paths, then something like the following \dict can be returned, the
# list being sorted "naturally" via the ''natsort'' module.
#
# python::
#     {'files': [PosixPath('/abs/path/readme/about.md'),
#                   PosixPath('/abs/path/readme/api.md'),
#                   PosixPath('/abs/path/readme/specs.md')]}
#
#
# [A "flat" \regex pattern]
#
# If ''data = {'regex': r".*\.md"}'' is used, and the \regex
# pattern finds paths directly in the parent folder, then something
# like the following \dict can be returned, the list being sorted
# "naturally" via the ''natsort'' module.
#
# python::
#     {'files': [PosixPath('/abs/path/readme/about.md'),
#                   PosixPath('/abs/path/readme/api.md'),
#                   PosixPath('/abs/path/readme/deps.md')]}
#
#
# [A recursive \regex pattern]
#
# If ''data = {'recreg': r".*\.md"}'' is used, and the \regex
# pattern finds paths recursively in the parent folder, then something
# like the following \dict can be returned, the list being sorted
# "naturally" via the ''natsort'' module. Note that here subfolders
# have been analyzed recursively.
#
# python::
#     {'files': [PosixPath('/abs/path/readme/about.md'),
#                PosixPath('/abs/path/readme/api.md'),
#                PosixPath('/abs/path/readme/api/extract.md'),
#                PosixPath('/abs/path/readme/api/use.md'),
#                PosixPath('/abs/path/readme/api/use/project.md'),
#                PosixPath('/abs/path/readme/api/use/project/date.md'),
#                PosixPath('/abs/path/readme/api/use/project/langs.md'),
#                PosixPath('/abs/path/readme/api/use/toc.md'),
#                PosixPath('/abs/path/readme/api/validate.md'),
#                PosixPath('/abs/path/readme/api/validate/affiliation.md'),
#                PosixPath('/abs/path/readme/api/validate/email.md'),
#                PosixPath('/abs/path/readme/api/validate/url.md'),
#                PosixPath('/abs/path/readme/deps.md')]}
###
def parser(
    parent: Path,
    data  : str | dict
) -> dict[str: Path | List[Path]]:
###
# Intrenal function to raise errors.
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
        return {kind: abspath}

# Pattern needs a one-level dict!
    if not isinstance(data, dict):
        _raisethis("one dict expecting for one glob or regex pattern")

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
        pattern = re.compile(pattern)

        all_abspaths = []

        meth = "glob" if kind == "regex" else "rglob"

        for fullpath in getattr(parent, meth)("*"):
            relpath = fullpath.relative_to(parent)

            if pattern.fullmatch(str(relpath)):
                all_abspaths.append(fullpath)

# Winning pattern?
    if not all_abspaths:
        _raisethis(f"no files found with the pattern")

    return {constants.TAG_TOC_PATH_FILES: natsorted(all_abspaths)}


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
    from pprint import pprint
    readme_dir = Path(__file__).parent.parent.parent.parent / "readme"

    pseudopath = "ap.md"
    pseudopath = ['glob', "*.md"]
    pseudopath = {'glob': "*.md", 'regex': r".*/pr.*\.md"}
    pseudopath = {'glb': "*.md"}

    pseudopath = "api.md"
    # pseudopath = "api/"
    # pseudopath = {'glob': "*.md"}
    pseudopath = {'regex': r".*\.md"}
    pseudopath = {'recreg': r".*\.md"}

    print(pseudopath)
    pprint(parser(readme_dir, pseudopath))
