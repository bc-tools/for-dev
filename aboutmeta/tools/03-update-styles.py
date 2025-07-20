#!/usr/bin/env python3

from collections import defaultdict
from pathlib     import Path

from black import (
    format_file_in_place,
    FileMode,
    WriteBack
)


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent

PROJECT_DIR  = THIS_DIR.parent
PROJECT_NAME = PROJECT_DIR.name

SRC_DIR    = PROJECT_DIR / "src" / PROJECT_NAME
PARSER_DIR = SRC_DIR / "parser"
STYLE_DIR  = SRC_DIR / "style"


TAG_INIT_FILE = "__init__.py"
INIT_FILE    = STYLE_DIR / TAG_INIT_FILE



TMPL_STYLE_PY = """
#!/usr/bin/env python3

# ---------------------------------------------------- #
# -- File created automatically.                    -- #
# --                                                -- #
# -- Formatting done by the Python project "black." -- #
# ---------------------------------------------------- #

from dataclasses import dataclass

{all_imports}


# --------------------- #
# -- DEFAULT PARSERS -- #
# --------------------- #

@dataclass
class Parsers:
    {all_attrs}
""".lstrip()


TMP_INIT_FILE = """
#!/usr/bin/env python3

# ---------------------------------------------------- #
# -- File created automatically.                    -- #
# --                                                -- #
# -- Formatting done by the Python project "black." -- #
# ---------------------------------------------------- #

{all_imports}

ALL_STYLES = {{
    {all_attrs}
}}
""".lstrip()

# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

all_parsers = defaultdict(list)

for pyfile in PARSER_DIR.glob("*/*.py"):
    if pyfile.name == TAG_INIT_FILE:
        continue

    pyfile = pyfile.relative_to(PARSER_DIR)

    parser = pyfile.parent.name
    style  = pyfile.stem

    all_parsers[style].append(parser)


for style, parsers in all_parsers.items():
    style_file = STYLE_DIR / f"{style}.py"

    parsers.sort()

    all_imports = []
    all_attrs   = []

    for parser in parsers:
        all_imports.append(
            f"import aboutmeta.parser.{parser}.default as {parser}_{style}"
        )

        all_attrs.append(
            f"{parser} = {parser}_{style}.parser"
        )

    all_imports = "\n".join(all_imports)
    all_attrs = "\n    ".join(all_attrs)

    pycode = TMPL_STYLE_PY.format(
        all_imports = all_imports,
        all_attrs   = all_attrs,
    )

    style_file.touch()
    style_file.write_text(pycode)

    format_file_in_place(
        style_file,
        fast       = False,
        mode       = FileMode(),
        write_back = WriteBack.YES,
    )

all_imports = []
all_attrs   = []

for style in all_parsers:
    all_imports.append(
        f"from .{style} import Parsers as {style.title()}Parsers"
    )

    all_attrs.append(
        f"'{style}': {style.title()}Parsers"
    )

all_imports = "\n".join(all_imports)
all_attrs = "\n    ".join(all_attrs)

pycode = TMP_INIT_FILE.format(
    all_imports = all_imports,
    all_attrs   = all_attrs,
)

INIT_FILE.touch()
INIT_FILE.write_text(pycode)

format_file_in_place(
    INIT_FILE,
    fast       = False,
    mode       = FileMode(),
    write_back = WriteBack.YES,
)
