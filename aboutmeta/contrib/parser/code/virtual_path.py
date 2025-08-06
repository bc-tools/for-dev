# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.core.errors import ParsingError

from pathlib import Path
import              re

from natsort import natsorted

# from aboutmeta.amdata         import AMData
from aboutmeta.core.constants import *
from aboutmeta.data           import tocpath


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TOCPathList = list[tocpath.TOCPath]

# A dedicated ''AMData'' object for list of ''tocpath'' objects.
# _AMDATA_TOCPATH_LIST = AMData()#flavour = BLOCK_TOC)



# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     parent : the parent directory of the path::''about.yaml’' file from which the ''data’' \arg comes.
#     data   : a virtual path that is either a relative path in the form of a string, a \glob or \regex pattern with the patterns provided using a single-key \dict.
#
#     :return: an instance of the class ''tocpath.TOCPath'' to work easily with the ''toc'' path: initial data, kind and absolute paths build.
#
#
# Let's look at some virtual examples where we assume that the parent folder has the absolute path path::“”/abs/path/readme''.
#
#
# [[An existing file]]
#
# Let's assume that the file path ::''/abs/path/readme/api.md'' exists. In this case, using ''data = "api.md"'' will imply the return of the following ''tocpath.TOCPath''. The use of a list can be understood by looking at the paths returned when using \glob or \regex patterns (see below).
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
# Let's assume that the folder path ::''/abs/path/readme/api'' exists. In this case, using ''data = "api/"'' will imply the return of the following ''tocpath.TOCPath'' indicating that the yaml::''toc'' block of an path::''about.yaml'' file need to be analyzed.
#
# python::
#     TOCPath(
#         data  = 'api/',
#         kind  = 'about',
#         paths = PosixPath('/abs/path/readme/api/about.yaml')})
#
#
# [[A "flat" \glob pattern]]
#
# If ''data = {'glob': "*.md"}'' is used, and the \glob pattern finds paths, then something like the following ''tocpath.TOCPath'' \obj can be returned, the list being sorted "naturally" via ''natsort'' module.
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
# [[A "recursive" \glob pattern]]
#
# If ''data = {'r-glob': "*.md"}'' is used, and the search will be done recursively giving something like the ''tocpath.TOCPath'' \obj below.
#
# python::
#     TOCPath(
#         data  = {'r-regex': '.*\\.md'},
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
#
#
# [[\regex patterns]]
#
# You can use \regexs for more advanced needs. The fist \glob pattern can be rewritten as ''data = {'regex': r"[^/]*\.md"}'', and the second one as ''data = {'r-regex': r"[^/]*\.md"}''.
###
def parse(
    parent: Path,
    data  : str | dict
) -> tocpath.TOCPath:
###
# Internal function to raise errors easily (the code is the \doc).
###
    def _raisethis(
        kind: str,
        xtra: str = ""
    ) -> None:
        if xtra:
            xtra = f"    + {xtra}"

        raise ParsingError(
            f"""
{kind}.
    + DATA: {data!r}
    + FILE: {parent}/about.yaml
{xtra}
            """.strip()
        )

###
# The standard value fir the  path::''about.yaml'' file.
###
    def _std() -> str:
# One-key dict used in the initial ''YAML'' file.
        if isinstance(data, dict):
            for k, v in data.items():
                return f"{k}: {v}"

# One string used in the initial ''YAML'' file.
        return data

###
# Let's go for the logical implementation.
###

# -- "Direct" path -- #

    if isinstance(data, str):
        is_dir = bool(data[-1] == "/")

# "Full" path resolved is useful.
        fullpath = parent / Path(data)
        fullpath = fullpath.resolve()

# Folder for an ''about.yaml'' file?
        if is_dir:
            if not fullpath.is_dir():
                _raisethis("inexistant folder")

            sub_yaml_file = fullpath / "about.yaml"

            if not sub_yaml_file.is_file():
                _raisethis("missing sub ''about.yaml'' file")

            recusearch = sub_yaml_file
            paths      = []

# File?
        else:
            if not fullpath.is_file():
                _raisethis("inexistant file")

            recusearch = None
            paths      = [fullpath]

# "Direct" path looks good.
        return tocpath.TOCPath(
            std        = _std(),
            recusearch = recusearch,
            paths      = paths
        )

# -- Pattern -- #

# We must have a one-key dict!
    if not isinstance(data, dict):
        _raisethis("one dict expected for one glob or regex pattern")

    if not len(data.keys()) == 1:
        _raisethis("one single key expected for a pattern dict")

    for kind, pattern in data.items(): # Python is funny...
        ...

# Legal key?
    kind = TAG_TOC_PATTERN_ABBREV.get(kind, kind)

    if not kind in TAG_TOC_PATTERN_KINDS:
        _raisethis(f"illegal pattern kind ''{kind}''")

# User has used an abbreviationthat we don't keep in the standard
# version of the data.
    if not kind in data:
        data = {kind: pattern}

# ''glob'' pattern.
    if kind in TAG_TOC_GLOB_PATTERNS:
        _glob = "glob"

        if kind == TAG_TOC_PATH_RECU_GLOB:
            _glob = f"r{_glob}"

        paths = [
            p
            for p in getattr(parent, _glob)(pattern)
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

        paths = []

        _glob = "glob" if kind == "regex" else "rglob"

        for fullpath in getattr(parent, _glob)("*"):
            relpath = fullpath.relative_to(parent)

            if pattern.fullmatch(str(relpath)):
                paths.append(fullpath)

# Winning pattern?
    if not paths:
        _raisethis(f"no files found with the pattern")

    return tocpath.TOCPath(
        std        = _std(),
        recusearch = None,
        paths      = natsorted(paths)
    )


### TODO
# prototype::
#     data : a ''tocpath.TOCPath'' list.
#
#     :return: the list obtained from data, adding any files from
#              the analysis of path::''about.yaml'' sub-files (cf.
#              the folders indicated in the toc blocks).
###
def map_list(data_list: TOCPathList) -> TOCPathList:
    final_paths = []

    for data in data_list:
        if data.kind == TAG_TOC_PATH_FILES:
            final_paths += data.paths

        else:
            _AMDATA_TOCPATH_LIST.build(yaml_file = data.paths)

            final_paths += _AMDATA_TOCPATH_LIST.data.toc

    return final_paths


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
    from pprint import pprint

    readme_dir = Path(__file__).parent.parent.parent.parent / "readme"

# BAD
    pseudopath = "ap.md"
    pseudopath = ['glob', "*.md"]
    # pseudopath = {'glob': "*.md", 'regex': r".*/pr.*\.md"}
    # pseudopath = {'glb': "*.md"}
    # pseudopath = {'regex': r".*(pr"}

# GOOD
    # pseudopath = "api.md"
    pseudopath = "api/"
    # pseudopath = {'glob': "*.md"}
    # pseudopath = {'rg': "*.md"}
    # pseudopath = {'regex': r"[^/]*\.md"}
    pseudopath = {'regex': '[^/]*\\.md'}
    # pseudopath = {'r-regex': r".*\.md"}

    print(pseudopath)

    tp = parse(readme_dir, pseudopath)

    # print(tp)

    pprint(tp)
