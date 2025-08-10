#!/usr/bin/env python3

# from rich import print

from .common     import *
from .need_tests import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

INIT_FILE    = "__init__.py"
INIT_CONTENT = "#!/usr/bin/env python3\n"


TAG_STATUS = "status"
TAG_OK     = "ok"


PATTERN_SECTION_COMMENT = re.compile(
    r"#\s+-+\s+#\n# --(.*)-- #\n# -+ #\n"
)

PATTERN_SUB_SECTION_COMMENT = re.compile(
    r"# ~~(.*)~~ #\n"
)


CTXT_DATA = "data"

CTXTS_AS_SECTIONS = [
    (CTXT_PARSER:= "parser"),
    (CTXT_MAPPER:= "mapper"),
]

SECTIONS_WITH_SUB_ONES = [
    (SECTION_CONSTANTS:= "CONSTANTS"),
    (SECTION_MAIN     := "MAIN"),
]

COMMON_SECTIONS_IGNORED = [
    (SECTION_TESTS:= "TESTS"),
    (SECTION_TOOLS:= "TOOLS"),
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


# ------------------ #
# -- CODE TO CODE -- #
# ------------------ #

def copy_paste_codes(
    context,
    this_dir,
    contrib_dir_name,
    nbtest,
):
    (
        projdir,
        projname,
        contribdir,
        statusdir,
        srcdir,
        testsdir
    ) = get_specs_folders(
        context          = context,
        this_dir         = this_dir,
        contrib_dir_name = contrib_dir_name,
        nbtest           = nbtest,
    )

    allfiles = get_accepted_paths(
        context    = context,
        contribdir = contribdir,
        statusdir  = statusdir,
    )

    if not allfiles:
        logging.warning("No file found!")

        return

# Let's build Python codes.
    logging.info(message_creation_update(context))

    add_missing_dir(srcdir)

    codes_added = set()

    for file in allfiles:
# Source code parts.
        code_parts = get_code_parts(
            file             = file,
            context          = context,
            sections_ignored = SECTIONS_IGNORED[context]
        )

        if not code_parts:
            continue

        something_done = True

        logging.info(
            log_title(
                title = context,
                desc  = file.name
            )
        )

# Final source code.
        final_code = get_final_code(
            code_parts,
            SECTIONS_IGNORED[context]
        )

# Lets's update the source code.
        src_file = srcdir / file.name
        src_file.touch()
        src_file.write_text(final_code + "\n")

        codes_added.add(file.stem)

# Extra files?
        xtra_files = get_xtra_files(file)

        if xtra_files:
            plurial = "s" if len(xtra_files) != 1 else ""

            logging.warning(f"Extra file{plurial} used.")

            for xfile in xtra_files:
                logging.warning(f"{xfile.name}")

                src_file = srcdir / xfile.name
                src_file.touch()
                src_file.write_text(xfile.read_text() + "\n")

# Nothing left expect the possible addition of an ''__init__.py'' file.
    add_missing_init(srcdir)

# Checking tests?
    if codes_added:
        missing_unit_tests(
            context,
            codes_added,
            projdir,
            testsdir,
        )


def get_code_parts(file, context, sections_ignored):
    content = file.read_text()

# 1st paring.
    parts   = dict()
    section = SECTION_MAIN

    for i, piece in enumerate(
        PATTERN_SECTION_COMMENT.split(content)
    ):
        piece = piece.strip()

        if i % 2 == 1:
            section = piece

        elif not section in sections_ignored:
            parts[section] = piece

    all_sections = list(parts)

# Missing mandatory "context" section?
    if (
        context in CTXTS_AS_SECTIONS
        and
        not context.upper() in all_sections
    ):
        return {}

# We have to clean MAIN and CONSTANTS secrtion by taking care
# of sub sections. This can make empty these sections.
    section_to_remove = []

    for section in parts:
        if section in SECTIONS_WITH_SUB_ONES:
            part = cleaned_part(
                parts[section],
                sections_ignored,
            )

            if part:
                parts[section] = part

            else:
                section_to_remove.append(section)

    for section in section_to_remove:
        del parts[section]

# Nothing left to do.
    return parts


def cleaned_part(
    part,
    sections_ignored,
):
    cleaned_part = []
    section      = SECTION_MAIN

    for i, piece in enumerate(
        PATTERN_SUB_SECTION_COMMENT.split(part)
    ):
        piece = piece.strip()

        if i % 2 == 1:
            section = piece

        elif not section in sections_ignored:
            cleaned_part.append(piece.strip())

    cleaned_part = '\n\n'.join(cleaned_part)

    return cleaned_part


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


def get_xtra_files(file):
    xtra_files = [
        p
        for p in file.parent.glob(
            f"{file.stem}-*"
        )
        if p != file
    ]

    return xtra_files
