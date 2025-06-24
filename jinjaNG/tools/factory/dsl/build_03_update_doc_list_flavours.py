#!/usr/bin/env python3

from btools.B01 import *


# ! -- DEBUGGING -- ! #
# Clear the terminal.
# print("\033c", end="")
# ! -- DEBUGGING -- ! #


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_FILE = Path(__file__)
THIS_DIR  = Path(THIS_FILE).parent

PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'jinjaNG'):
   PROJECT_DIR = PROJECT_DIR.parent

THIS_FILE_REL_SRC_PATH    = Path(__file__) - PROJECT_DIR
THIS_FILE_REL_PROJECT_DIR = THIS_FILE - PROJECT_DIR


DOC_CONTRIB_DIR = PROJECT_DIR / 'doc' / 'content' / 'contribute'
DOC_CONTRIB_DSL = DOC_CONTRIB_DIR / 'api' / 'dsl.txt'


CONTRIB_DSL_DIR    = PROJECT_DIR / 'contribute' / 'api' / 'dsl'
README_CONTRIB_DSL = CONTRIB_DSL_DIR / 'README.md'


FLAVOURS_STATUS_YAML = THIS_DIR / 'flavours.yaml'


# ----------------------- #
# -- SPECS STATUS YAML -- #
# ----------------------- #

print(f"{TAB_1}* Updating the list of flavours in the docs.")

with FLAVOURS_STATUS_YAML.open(
    mode     = "r",
    encoding = "utf-8"
) as f:
    flavours_by_status = yaml_load(f)

# ! -- DEBUGGING -- ! #
# print(flavours_by_status)
# exit()
# ! -- DEBUGGING -- ! #


# ------------------- #
# -- THE HUMAN DOC -- #
# ------------------- #

print(f"{TAB_2}+ List for the human doc.")

maxlen = max(
    len(fl)
    for fl in flavours_by_status[STATUS_OK]
)

autolist = '\n'.join(
      ' '*4 + f'* ¨{fl} ' + ' '*(maxlen - len(fl))
    + f'via python::''FLAVOUR_{fl.upper()} = "{fl}"''.'
    for fl in flavours_by_status[STATUS_OK]
)

autoupdate(
    onefile     = DOC_CONTRIB_DSL,
    magiccode   = '// -- ALL FLAVOURS - AUTO LIST - START -- //',
    autocontent = '\n' + autolist + '\n'
)


# ------------------ #
# -- THE TECH DOC -- #
# ------------------ #

print(f"{TAB_2}+ List for the technical doc.")

# Alphabetic list of the flavours.

flavours_and_their_status = {
    fl: st
    for st, all_fl in flavours_by_status.items()
    for fl in all_fl
}

# ! -- DEBUGGING -- ! #
# print(flavours_and_their_status)
# exit()
# ! -- DEBUGGING -- ! #

autolist = []

all_flavours = sorted(flavours_and_their_status.keys())

for fl in all_flavours:
    st = flavours_and_their_status[fl]

    autolist.append(' '*2 + f"* **[{st}]** `{fl}`")

autolist = '\n'.join(autolist)

autoupdate(
    onefile     = README_CONTRIB_DSL,
    magiccode   = '<!-- LIST OF FLAVOURS AND THEIR STATUS - AUTO - START -->',
    autocontent = '\n' + autolist + '\n'
)

# List of statuses with the relevant flavours.

autolist = []

for st in sorted(flavours_by_status):
    autolist.append(' '*2 + f"* Status **''{st}''**")

    for fl in flavours_by_status[st]:
        autolist.append(' '*4 + f"+ `{fl}`")

autolist = '\n'.join(autolist)

autoupdate(
    onefile     = README_CONTRIB_DSL,
    magiccode   = '<!-- LIST OF STATUSES WITH THE RELEVANT FLAVOURS - AUTO - START -->',
    autocontent = '\n' + autolist + '\n'
)
