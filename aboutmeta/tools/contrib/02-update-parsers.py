#!/usr/bin/env python3

from pathlib import Path
import              re
from yaml    import safe_load

# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR     = Path(__file__).parent
PROJECT_DIR  = THIS_DIR.parent.parent
PROJECT_NAME = PROJECT_DIR.name

CONTRIB_DIR = PROJECT_DIR / "contrib"
SRC_DIR     = PROJECT_DIR / "src" / PROJECT_NAME

TAB_1 = ' '*2
TAB_2 = TAB_1*2

TAG_STATUS = "status"
TAG_OK     = "ok"


PATTERN_MAGIC_COMMENT = re.compile(
    r"#\s+-+\s+#\n# --(.*)-- #\n# -+ #\n"
)

CTXTS_FOR_CONTRIB = [
    (CTXT_MAIN := "MAIN"),
    (CTXT_TESTS:= "HUMAN TESTS"),
]

CTXTS_FOR_CODE = [
    (CTXT_IMPORTS  := "IMPORTS"),
    (CTXT_CONSTANTS:= "CONSTANTS"),
    (CTXT_IMPLEMENT:= "IMPLEMENTATION"),
]

CTXTS_FOR_TOOLS = [
    (CTXT_TOOLS:= "TOOLS"),
]

ALL_CTXTS = CTXTS_FOR_CONTRIB + CTXTS_FOR_CODE + CTXTS_FOR_TOOLS


PATTERN_ABOUTMETA_IMPORTS = re.compile(
    fr"\b(aboutmeta\.(?P<kind>data|tool)\.)(?P<module>\w+)(?P<used>.\w+)+\b"
)

TMPL_INTERNAL_IMPORT = "from ....{} import {}"

# ----------- #
# -- TOOLS -- #
# ----------- #

def get_relpaths(onedir):
# WARNING! "No status" implies "No parser to add".
    status_dir = onedir / "STATUS"
    files      = []

    for yaml_file in status_dir.glob("**/*.yaml"):
        status_data = safe_load(yaml_file.read_text())

        if status_data[TAG_STATUS] != TAG_OK:
            continue

        reldir       = yaml_file.relative_to(status_dir)
        relpath      = reldir.parent / f"{reldir.stem}.py"
        contrib_file = onedir / relpath

        if not contrib_file.is_file():
            raise IOError(f"missing file:\n{contrib_file}")

        files.append((relpath, contrib_file))

    return files


def get_code_parts(content):
# Contexts unchanged.
    ctxt  = "MAIN"
    parts = {
        CTXT_IMPORTS: ""
    }

    for i, piece in enumerate(PATTERN_MAGIC_COMMENT.split(content)):
        if i % 2 == 1:
            ctxt = piece.strip()

            if not ctxt in ALL_CTXTS:
                raise ValueError(
                    f"unkwon magic title comment ''{ctxt}''."
                )

        else:
            parts[ctxt] = piece.strip()

# Management of the aboutmeta internal imports.
    newlines         = []
    internal_imports = set()

    for line in parts[CTXT_IMPLEMENT].split('\n'):
        linecode, *comment = line.split("#")

        if linecode:
            match = PATTERN_ABOUTMETA_IMPORTS.search(linecode)

            if match:
                comment = '#' + '#'.join(comment)

                before = linecode[:match.start()]
                after = linecode[match.end():]

                line = (
                    before
                    + match.group('module')
                    + match.group('used')
                    + after
                    + comment
                )

                internal_imports.add(
                    TMPL_INTERNAL_IMPORT.format(
                        match.group('kind'),
                        match.group('module')
                    )
                )

        newlines.append(line)

    parts[CTXT_IMPLEMENT] = '\n'.join(newlines)

    if internal_imports:
        internal_imports = list(internal_imports)
        internal_imports.sort()

        internal_imports = '\n'.join(internal_imports)

        parts[CTXT_IMPORTS] = f"{internal_imports}\n\n{parts[CTXT_IMPORTS]}"
        parts[CTXT_IMPORTS] = parts[CTXT_IMPORTS].strip()

# Nothing left todo.
    return parts


def get_src_code(code_parts):
    code = []

    for tag in CTXTS_FOR_CODE:
        if tag in code_parts:
            code += [
                '',
                '',
                magic_comment(tag),
                '',
                code_parts[tag]
            ]

    code = '\n'.join(code)
    code = code.strip()

    return code


def magic_comment(title):
    title = f"-- {title} --"

    rule = '-'*len(title)
    rule = f"# {rule} #"

    title = f"""
{rule}
# {title} #
{rule}
    """.strip()

    return title


# ------------ #
# -- PARSER -- #
# ------------ #

# Source codes.
parser_contrib_dir = CONTRIB_DIR / "parser"
parser_src_dir = SRC_DIR / "parser"

for relpath, contrib_file in get_relpaths(parser_contrib_dir):
    print(f"+ ''{relpath}'' new parser.")

    code_parts = get_code_parts(contrib_file.read_text())

    if CTXT_TOOLS in code_parts:
        print(f"{TAB_2}> This parser use tools.")

    code = get_src_code(code_parts)

    src_file = parser_src_dir / relpath

    src_file.parent.mkdir(
        parents  = True,
        exist_ok = True
    )

    src_file.touch()
    src_file.write_text(code)

# Files for unit tests?
