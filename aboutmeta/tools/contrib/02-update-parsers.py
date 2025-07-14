#!/usr/bin/env python3

from collections import defaultdict
from pathlib     import Path
import                  re
from yaml        import safe_load


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR     = Path(__file__).parent
PROJECT_DIR  = THIS_DIR.parent.parent
PROJECT_NAME = PROJECT_DIR.name

CONTRIB_DIR = PROJECT_DIR / "contrib" / "parser"
SRC_DIR     = PROJECT_DIR / "src" / PROJECT_NAME / "parser"
TESTS_DIR   = PROJECT_DIR / "tests" / "parser"

INIT_FILE    = "__init__.py"
INIT_CONTENT = "#!/usr/bin/env python3\n"


TAB_1 = ' '*2
TAB_2 = TAB_1*2

ITEM_1 = '+'
ITEM_2 = f'{TAB_1}*'
ITEM_3 = f'{TAB_2}-->'

TAG_STATUS = "status"
TAG_OK     = "ok"


PATTERN_MAGIC_COMMENT = re.compile(
    r"#\s+-+\s+#\n# --(.*)-- #\n# -+ #\n"
)

PATTERN_TEST_NAME =re.compile(r"test_.*_\d+_(?P<syntax>.+)")

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


# ------------------ #
# -- SOURCE CODES -- #
# ------------------ #

print(f"{ITEM_1} Creation/update of source code...")

contrib_files = defaultdict(set)
dirs_created  = set()

for relpath, contrib_file in get_relpaths(CONTRIB_DIR):
    print(f"{ITEM_2} ''{relpath}'' new parser.")

    data_type = str(relpath.parents[0])
    syntax    = relpath.stem

    contrib_files[data_type].add(syntax)

    code_parts = get_code_parts(contrib_file.read_text())

    if CTXT_TOOLS in code_parts:
        print(f"{ITEM_3} This parser use tools.")

    code = get_src_code(code_parts)

    src_file = SRC_DIR / relpath

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


# --------------------------- #
# -- FILES FOR UNIT TESTS? -- #
# --------------------------- #

print(f"{ITEM_1} Verifying the existence of test files...")

test_files  = defaultdict(set)
no_pb_found = True

for test_file in TESTS_DIR.glob("*/*/test_*.py"):
    test_file = test_file.relative_to(TESTS_DIR)

    data_type = str(test_file.parents[0])
    syntax    = test_file.stem

    match = PATTERN_TEST_NAME.search(syntax)

    if match:
        test_files[data_type].add(match.group("syntax"))

for data_type, syntaxes in contrib_files.items():
    if not data_type in test_files:
        no_pb_found = False

        print(f"{ITEM_2} Zero test files for ''{data_type}'' parsers.")

    elif test_files[data_type] != contrib_files[data_type]:
        no_pb_found = False

        unexpected = test_files[data_type] - contrib_files[data_type]
        missing    = contrib_files[data_type] - test_files[data_type]

        if missing:
            print(f"{ITEM_2} Missing test files for ''{data_type}'' parsers.")

            missing = list(missing)
            missing.sort()
            missing = f"\n{ITEM_3}".join(missing)

            print(f"{ITEM_3} {missing}")

        if unexpected:
            print(f"{ITEM_2} Unexpected test files for ''{data_type}'' parsers.")

            unexpected = list(unexpected)
            unexpected.sort()
            unexpected = f"\n{ITEM_3}".join(unexpected)

            print(f"{ITEM_3} {unexpected}")

if no_pb_found:
    print(f"{ITEM_2} No test files missing.")
