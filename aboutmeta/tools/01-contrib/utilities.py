#!/usr/bin/env python3

from pprint import pprint

from collections import defaultdict
from pathlib     import Path
import                  re

from yaml import safe_load


# --------------- #
# -- CONSTANTS -- #
# --------------- #

INIT_FILE    = "__init__.py"
INIT_CONTENT = "#!/usr/bin/env python3\n"


TAB_1 = ' '*2
TAB_2 = TAB_1*2
TAB_3 = TAB_1*3

ITEM_1 = '+'
ITEM_2 = f'{TAB_1}*'
ITEM_3 = f'{TAB_2}-'
ITEM_4 = f'{TAB_3}-->'


TAG_STATUS = "status"
TAG_OK     = "ok"


PATTERN_MAGIC_COMMENT = re.compile(
    r"#\s+-+\s+#\n# --(.*)-- #\n# -+ #\n"
)

PATTERN_TEST_NAME =re.compile(r"test_.*_\d+_(?P<syntax>.+)")


CTXT_DATA   = "data"
CTXT_PARSER = "parser"
CTXT_MAPPER = "mapper"

SECTION_MAIN = "MAIN"

COMMON_SECTIONS_IGNORED = [
    (SECTION_TESTS := "TESTS"),
    (SECTION_TOOLS := "TOOLS"),
]

SECTIONS_IGNORED = {
    CTXT_DATA  : COMMON_SECTIONS_IGNORED,
    CTXT_PARSER: COMMON_SECTIONS_IGNORED + [
        (SECTION_MAPPER:= "MAPPER")
    ],
    CTXT_MAPPER: COMMON_SECTIONS_IGNORED + [
        (SECTION_PARSER:= "PARSER")
    ],
}


# ----------- #
# -- PATHS -- #
# ----------- #

def get_folders(
    this_dir,
    context,
    nbtest,
):
    projdir  = this_dir.parent.parent
    projname = projdir.name

    contribdir = projdir / "contrib" / context / "code"
    statusdir  = contribdir.parent / "status"
    src     = projdir / "src" / projname / context
    tests   = projdir / "tests" / f"{nbtest}-{context}"

    return (
        projdir,
        projname,
        contribdir,
        statusdir,
        src,
        tests
    )


# WARNING!
# "No status" ==> "No parser to add"
def get_accepted_paths(
    contribdir,
    statusdir,
):
    files = []

    for yaml_file in statusdir.glob("*.yaml"):
        statusdata = safe_load(yaml_file.read_text())

        if statusdata[TAG_STATUS] != TAG_OK:
            continue

        file = contribdir / f"{yaml_file.stem}.py"

        if not file.is_file():
            raise IOError(f"missing file:\n{file}")

        files.append(file)

    files.sort()

    return files


# ------------ #
# -- SOURCE -- #
# ------------ #

def copy_paste_files(
    this_dir,
    context,
    nb_test,
):
    (
        projdir,
        projname,
        contribdir,
        statusdir,
        src,
        tests
    ) = get_folders(
        this_dir,
        context,
        nb_test,
    )

    allfiles = get_accepted_paths(
        contribdir,
        statusdir,
    )

    if not allfiles:
        print(f"{ITEM_2} No file found!")

        return None

    for file in allfiles:
        print(f"{ITEM_2} [{context}]  {file.name}")

# Source code parts.
        code_parts = get_code_parts(
            file    = file,
            context = context
        )

# Tools used?
        if code_parts.get(SECTION_TOOLS, ""):
            print(f"{ITEM_3} Dev tools available.")

# Final source code.
        final_code = get_final_code(
            code_parts,
            SECTIONS_IGNORED[context]
        )

# Lets's update the source code.
        src_file = src / file.name

        src_file.parent.mkdir(
            parents  = True,
            exist_ok = True
        )

        src_file.touch()
        src_file.write_text(final_code + "\n")

# Extra files?
        xtra_files = get_xtra_files(file, context)

        if xtra_files:
            plurial = "s" if len(xtra_files) != 1 else ""

            print(f"{ITEM_3} Extra file{plurial} used.")

            for xfile in xtra_files:
                print(f"{ITEM_4} {xfile.name}")

                src_file = src / xfile.name
                src_file.touch()
                src_file.write_text(xfile.read_text() + "\n")

# Nothing left expect the addition of an ''__init__.py'' file.
    initfile = src / INIT_FILE

    initfile.touch()
    initfile.write_text(INIT_CONTENT)


def get_code_parts(file, context):
    content = file.read_text()

    parts   = dict()
    section = SECTION_MAIN

    for i, piece in enumerate(
        PATTERN_MAGIC_COMMENT.split(content)
    ):
        piece = piece.strip()

        if i % 2 == 1:
            section = piece

        else:
            parts[section] = piece

    return parts


def get_final_code(code_parts, sections_ignored):
    code = []

    for section, part in code_parts.items():
        if section in sections_ignored:
            continue

        code += [
            '',
            '',
            magic_comment(section),
            '',
            part
        ]

    code = '\n'.join(code)
    code = code.strip()

    return code


def magic_comment(section):
    if section == SECTION_MAIN:
        return ""

    section = f"-- {section} --"

    rule = '-'*len(section)
    rule = f"# {rule} #"

    section = f"""
{rule}
# {section} #
{rule}
    """.strip()

    return section


def get_xtra_files(file, context):
    xtra_files = [
        p
        for p in file.parent.glob(
            f"{context}-{file.stem}-*"
        )
        if p != file
    ]

    return xtra_files
