###   HELPER
# Let's look at some virtual examples where we assume that the
# yaml file folder has absolute path path::''/abs/path/readme''.
#
#
# [[An existing file]]
#
# Let's assume that the file path ::''/abs/path/readme/api.md''
# exists. In this case, using ''data = "api.md"'' will imply the
# return of the following ''TOCPath'' \obj. The use of a list
# can be understood by looking at the paths returned when using
# \glob or \regex patterns (see below).
#
# python::
#     TOCPath(
#         std        = 'api/md',
#         postsearch = None,
#         paths      = [PosixPath('/abs/path/readme/api.md')])
#
#
# [[An existing folder]]
#
# Let's assume that the folder path ::''/abs/path/readme/api''
# exists. In this case, using ''data = "api/"'' will imply the
# return of the following ''TOCPath'' \obj indicating that the
# yaml::''toc'' block of an path::''about.yaml'' file need to
# be analyzed during of post action.
#
# python::
#     TOCPath(
#         std        = 'api/',
#         postsearch = PosixPath('/abs/path/readme/api/about.yaml',
#         paths      = [])
#
#
# [[A "flat" \glob pattern]]
#
# If ''data = {'glob': "*.md"}'' is used, and the \glob pattern
# finds paths, then something like the following ''TOCPath''
# \obj can be returned, the list being sorted "naturally" via
# ''natsort'' module.
#
# python::
#     TOCPath(
#         std        = "glob: '*.md'",
#         postsearch = None,
#         paths      = [PosixPath('/abs/path/readme/about.md'),
#                       PosixPath('/abs/path/readme/api.md'),
#                       PosixPath('/abs/path/readme/specs.md')])
#
#
# [[A "recursive" \glob pattern]]
#
# If ''data = {'r-glob': "*.md"}'' is used, and the search will
# be done recursively giving something like the ''TOCPath'' \obj
# below.
#
# python::
#     TOCPath(
#         std        = "r-glob: '*.md'",
#         postsearch = None,
#         paths      = [PosixPath('/abs/path/readme/about.md'),
#                       PosixPath('/abs/path/readme/api.md'),
#                       PosixPath('/abs/path/readme/api/extract.md'),
#                       PosixPath('/abs/path/readme/api/use.md'),
#                       PosixPath('/abs/path/readme/api/use/project.md'),
#                       PosixPath('/abs/path/readme/api/use/toc.md'),
#                       PosixPath('/abs/path/readme/api/validate.md'),
#                       PosixPath('/abs/path/readme/api/validate/email.md'),
#                       PosixPath('/abs/path/readme/api/validate/url.md'),
#                       PosixPath('/abs/path/readme/deps.md')])
#
#
# [[\regex patterns]]
#
# You can use \regexs for more advanced needs. The first \glob
# pattern can be rewritten as ''data = {'regex': r".*\.md"}'',
# and the second one as ''data = {'r-regex': r".*\.md"}''.
###








def _parse_direct_path(
    about_file_dir: Path,
    data          : str
) -> TOCPath:
    is_dir = bool(data[-1] == "/")

# Folder for an ''about.yaml'' file?
    if is_dir:
        if not fullpath.is_dir():
            _raisethis(
                about_file_dir = about_file_dir,
                data           = data,
                message        = "inexistant folder.",
                xtra           = f"FOLDER: {fullpath}"
            )

        sub_yaml_file = fullpath / "about.yaml"

        if not sub_yaml_file.is_file():
            _raisethis(
                about_file_dir = about_file_dir,
                data           = data,
                message        = (
                    "folder without an ''about.yaml'' file."
                ),
                xtra           = f"FOLDER: {fullpath}"
            )

        postsearch = sub_yaml_file
        paths      = []

# File?
    else:
        if not fullpath.is_file():
            _raisethis(
                about_file_dir  = about_file_dir,
                data            = data,
                message         = "path not pointing to a file."
            )
