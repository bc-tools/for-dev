#!/usr/bin/env python3

from btools.B01 import *


# ! -- DEBUGGING -- ! #
# Clear the terminal.
# print("\033c", end="")
# ! -- DEBUGGING -- ! #


#!/usr/bin/env python3

from datetime import datetime
from pathlib  import Path
from yaml     import safe_load as yaml_load

from mistool.string_use import between


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_FILE = Path(__file__)
THIS_DIR  = Path(THIS_FILE).parent


THIS_FILE = Path(__file__)
THIS_DIR  = Path(THIS_FILE).parent

DOC_DIR = THIS_DIR

while(DOC_DIR.name != 'jinjaNG'):
   DOC_DIR = DOC_DIR.parent

DOC_DIR = DOC_DIR / 'doc'


SPE_VARS_DOCFILE = DOC_DIR / 'content' / 'how-to' / 'cli' / 'hooks' / 'spevars.txt'


with(THIS_DIR / "spevars.yaml").open(
    encoding = 'utf-8',
    mode     = 'r'
) as f:
    SPEVARS = yaml_load(f)


TEMPLATE_ONEPATH = ' '*4 + (
    "1) jinjang::''{name}'' est le chemin complet du fichier {desc}."
    "\n"
    "    Pour ne pas garder l'extension, il suffit d'employer "
    "jinjang::''{name}_stem''."
)


# --------------- #
# -- LET' WORK -- #
# --------------- #

paths_content = []

for name, desc in SPEVARS['paths'].items():
    paths_content.append(
        TEMPLATE_ONEPATH.format(
            name = name,
            desc = desc
        )
    )

paths_content = '\n\n'.join(paths_content)


last_content = SPE_VARS_DOCFILE.read_text(encoding = 'utf-8')

before, _, after = between(
    text = last_content,
    seps = [
        "/* -- SPE. VARS - START -- */",
        "/* -- SPE. VARS - END -- */",
    ],
    keepseps = True
)


new_content = f"{before}\n\n{paths_content}\n\n{after}"


if new_content != last_content:
    print('    * DOC - Hooks. Updating the list of specials vars.')

    before, last_date, after = between(
        text = new_content,
        seps = [
            "this::\n    date =",
            "\n",
        ],
        keepseps = True
    )

    last_date = last_date.strip()
    last_date = datetime.strptime(last_date, '%Y-%m-%d')
    now       = datetime.now()

    if now > last_date:
        now = datetime.now()
        now = now.strftime('%Y-%m-%d')

        new_content = f"{before} {now}{after}"

        SPE_VARS_DOCFILE.write_text(
            data     = new_content,
            encoding = 'utf-8'
        )
