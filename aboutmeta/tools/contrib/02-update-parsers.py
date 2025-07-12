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


INIT_FILE    = "__init__.py"
INIT_CONTENT = "#!/usr/bin/env python3\n"


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

dirs_created = set()

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

    dirs_created.add(src_file.parent)

    src_file.touch()
    src_file.write_text(code)

# Just add ''__init__.py'' files.
for onedir in dirs_created:
    initfile = onedir / INIT_FILE

    initfile.touch()
    initfile.write_text(INIT_CONTENT)

# Do we have files for unit tests?
