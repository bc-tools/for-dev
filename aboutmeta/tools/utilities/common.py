#!/usr/bin/env python3

# Rich colors: python -m rich.color

from typing import Any

import                   logging
from rich.logging import RichHandler
from rich.console import Console

import              ast
from copy    import copy
from pathlib import Path
import              re

import           tomli
from yaml import safe_load

from black import (
    format_str,
    format_file_in_place,
    FileMode,
    WriteBack
)


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAG_INIT     = "__init__"
INIT_FILE    = f"{TAG_INIT}.py"
INIT_CONTENT = "#!/usr/bin/env python3\n"

TAG_CONSTANTS = "constants"
TAG_SIGNS     = "signatures"
TAG_SPECS     = "specs"
TAG_FLAVOURS  = "flavours"

CONSTANTS_FILE = f"{TAG_CONSTANTS}.py"
SIGNS_FILE     = f"{TAG_SIGNS}.py"
SPECS_FILE     = f"{TAG_SPECS}.py"
FLAVOURS_FILE  = f"{TAG_FLAVOURS}.py"

TAG_OPTIONAL   = '*'

TAG_STATUS = "status"
TAG_OK     = "ok"

TAG_BAD_VALIDATION = "bad validation"
TAG_FILE           = "file"

TAG_CRITICAL = "critical"
TAG_WARNING  = "warning"

META_TAGS = [
    TAG_SPECS_ALT_ALL   := "__ALT_ALL__",
    TAG_SPECS_ALT_TUPLES:= "__ALT_TUPLES__",
    TAG_SPECS_BLOCK     := "__BLOCK__",
    TAG_SPECS_CONTENT   := "__CONTENT__",
    TAG_SPECS_DATA      := "__DATA__",
    TAG_SPECS_LIST_OF   := "__LIST_OF__",
    TAG_SPECS_MAPPER    := "__MAPPER__",
    TAG_SPECS_PARSER    := "__PARSER__",
    TAG_SPECS_REQUIRED  := "__REQUIRED__",
    TAG_SPECS_OPTIONAL  := "__OPTIONAL__",
    TAG_SPECS_TOOLS     := "__TOOLS__",
    TAG_SPECS_TYPE      := "__TYPE__",
]

# --------------- #
# -- TEMPLATES -- #
# --------------- #

TEMPL_CODE_HEADER = """
#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #
""".strip()


# ------------------------------- #
# -- LOGGING "DYNAMIC" CONFIG. -- #
# ------------------------------- #

LOG_FILE = "tools.log"


###
# XXXXXXX
###
class FileFormatter(logging.Formatter):
    def format(self, record):
        original_message = record.getMessage()
        cleaned_message  = re.sub(r'\[.*?\]', '', original_message)

        record.msg        = cleaned_message
        formatted_message = super().format(record)
        record.msg        = original_message

        return formatted_message


###
# XXXXXXX
###
class ColorFilter(logging.Filter):
    def filter(self, record):
        original_levelname = record.levelname

        if record.levelno >= logging.CRITICAL:
            record.msg = f"[black on wheat1]{record.msg}[/black on wheat1]"

        elif record.levelno >= logging.ERROR:
            record.msg = f"[bright_red]{record.msg}[/bright_red]"

        elif record.levelno >= logging.WARNING:
            record.msg = f"[dark_goldenrod]{record.msg}[/dark_goldenrod]"

        return True


###
# prototype::
#     no_color  : set to ''False'', the log information will be
#                 printed in color; otherwise, it will be printed
#                 in black and white.
#
#     :action: the function lives up to its name...
###
def setup_logging(no_color = False) -> None:
# Terminal handler
#
# ''color_system = "auto"'' detects whether the output is a real
# terminal. If not—such as when output is redirected via a pipe—no
# color is used
    console = Console(
        stderr=True,
        color_system=None if no_color else "auto"
    )

# File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="a"
    )
    file_handler.setLevel(logging.ERROR)

    file_formatter = FileFormatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
    file_handler.setFormatter(file_formatter)

# Terminal handler
    term_handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        markup=True
    )
    term_handler.setLevel(logging.INFO)

# Apply global config
    logging.basicConfig(
# Resetting configurations
        force=True,
        level=logging.INFO,
        handlers=[term_handler, file_handler],
    )

# Appliquer le filtre UNIQUEMENT au gestionnaire de la console
    term_handler.addFilter(ColorFilter())


###
# XXXXXXX
###
setup_logging()


# ---------------------- #
# -- LOGGING MESSAGES -- #
# ---------------------- #

###
# XXXXXXX
###
def log_title(
    title,
    desc,
):
    return f"{title.upper()} - {desc}"

###
# XXXXXXX
###
def message_creation_update(
    context,
    upper   = True,
    plurial = True,
):
    if upper:
        context = context.upper()

    plurial = 's' if plurial else ''

    return f"{context} code{plurial}: creation or update."


def raise_validation_error(
    key,
    yfile_name,
    desc,
    xtra = ""
):
    if key:
        key = f"'{key}' key in "

    desc = f"See {key}'{yfile_name}' file: {desc}"

    logging.error(
        log_title(
            TAG_BAD_VALIDATION,
            desc = desc
        )
    )

    if xtra:
        xtra = f" {xtra}"

    raise ValueError(f"{desc}{xtra}")


# ----------- #
# -- PATHS -- #
# ----------- #

def get_specs_folders(
    context,
    this_dir,
    contrib_dir_name,
    nbtest,
    subfolder = "code",
):
    projdir  = this_dir.parent.parent
    projname = projdir.name

    contribdir = projdir / "contrib" / contrib_dir_name / subfolder
    statusdir  = contribdir.parent / "status"
    srcdir     = projdir / "src" / projname / TAG_SPECS / context
    testsdir   = projdir / "tests" / f"{nbtest:02d}-{context}"

    return (
        projdir,
        projname,
        contribdir,
        statusdir,
        srcdir,
        testsdir
    )


# WARNING!
# "No status" ==> "No parser to add"
def get_accepted_paths(
    context,
    contribdir,
    statusdir,
    subfolder = "",
    ext       = 'py',
):
    logging.info(
        f"{context.upper()} - Looking for accepted contribs."
    )

    files = []

    if subfolder:
        subfolder += "/"

    for yaml_file in statusdir.glob(
        f"{subfolder}*.yaml"
    ):
        statusdata = safe_load(yaml_file.read_text())

        if statusdata[TAG_STATUS] != TAG_OK:
            continue

        file = contribdir / f"{yaml_file.stem}.{ext}"

        if not file.is_file():
            raise IOError(f"missing file:\n{file}")

        files.append(file)

    files.sort()

    return files


# --------------------- #
# -- FOLDERS / FILES -- #
# --------------------- #

def add_missing_dir(dirpath):
    if not dirpath.is_dir():
        dirpath.mkdir(
            parents  = True,
            exist_ok = True
        )

        logging.warning(f"Folder added: '{dirpath}'")


def add_missing_init(srcdir):
    # Nothing left expect the addition of an ''__init__.py'' file.
    initfile = srcdir / INIT_FILE

    if not initfile.is_file():
        initfile.touch()
        initfile.write_text(INIT_CONTENT)

        logging.info("__init__.py file added.")


def add_black_pyfile(
    code,
    file
):
    file.write_text(code)

    format_file_in_place(
        file,
        fast       = False,
        mode       = FileMode(),
        write_back = WriteBack.YES,
    )


def append_black_pyfile(
    code,
    file,
    nbempty = 1
):
    code = format_str(
        code,
        mode = FileMode()
    )
    code = '\n' * nbempty + code
    code = file.read_text() + code

    file.write_text(code)


# --------------------- #
# -- PYTHON ANALYSIS -- #
# --------------------- #

def get_parse_signature(
    file,
    func_name
):
    src_code  = Path(file).read_text()
    tree      = ast.parse(src_code)
    arguments = []

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.FunctionDef)
            and
            node.name == func_name
        ):
            args = [arg.arg for arg in node.args.args]

            # for i, default in enumerate(node.args.defaults, start=len(args)-len(node.args.defaults)):
            #     args[i] += f"={ast.unparse(default)}"

            return args

    return None


def get_metatags(
    allvars,
    vals = META_TAGS
):
    return [
        vname
        for vname in allvars
        if allvars[vname] in vals
    ]


def code_with_metatags(
    allvars,
    metavars,
    code
):
    for name in metavars:
        code = code.replace(f"{allvars[name]!r}", name)

    return code


def get_pyname(yaml_name):
    pyname = yaml_name

    for (old, new) in [
        ('-', '_'),
    ]:
        pyname = pyname.replace(old, new)

    return pyname


# --------------------- #
# -- YAML ANALYSIS -- #
# --------------------- #

def get_name_required(name):
    if name[-1] == TAG_OPTIONAL:
        is_required = False
        name        = name[:-1].strip()

    else:
        is_required = True
        name        = name

    return name, is_required



# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    setup_logging()
    logging.info("One information.")
    # logging.debug("Debugging?")
    logging.warning("One warning!")
    logging.error("An error!")
    logging.critical("A critical error!")
