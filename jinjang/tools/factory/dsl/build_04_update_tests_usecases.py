#!/usr/bin/env python3

from btools.B01 import *


# ! -- DEBUGGING -- ! #
# Clear the terminal.
print("\033c", end="")
# ! -- DEBUGGING -- ! #


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_FILE = Path(__file__)
THIS_DIR  = Path(THIS_FILE).parent

PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'jinjaNG'):
   PROJECT_DIR = PROJECT_DIR.parent


CONTRIB_DSL_DIR    = PROJECT_DIR / 'contribute' / 'api' / 'dsl'
TESTS_USECASES_DIR = PROJECT_DIR / 'tests' / 'usecases' / 'datas'


FLAVOURS_STATUS_YAML = THIS_DIR / 'flavours.yaml'


addfindsrc(
    file    = __file__,
    project = 'jinjaNG',
)

from src import AUTO_FROM_EXT


# ------------------------ #
# -- USECASES FOR TESTS -- #
# ------------------------ #

print(f"{TAB_1}* Updating datas for tests build on the usecases.")

# We can't update usecases for an evolving flavour, this is why we use
# ``FLAVOURS_STATUS_YAML``, and not ``config.flavour.SETTINGS``.

with FLAVOURS_STATUS_YAML.open(
    mode     = "r",
    encoding = "utf-8"
) as f:
    flavours_OK = yaml_load(f)[STATUS_OK]


for fl in flavours_OK:
    srcfiles = []

    usecase_dir   = CONTRIB_DSL_DIR / fl / 'usecases'
    flavours_exts = AUTO_FROM_EXT[fl]

# New flavour datas dir.
    flavour_dest_dir = TESTS_USECASES_DIR / fl

    if flavour_dest_dir.is_dir():
        flavour_dest_dir.remove()

# Copying the datas.
    for pdir in usecase_dir.glob('*'):
        if(
            not pdir.is_dir()
            or
            pdir.name.startswith('.')
            or
            pdir.name.startswith('x-')
        ):
            continue

        for pfile in pdir.glob('*'):
            name = pfile.stem

            if(
                not pfile.is_file()
                or
                not name in ['datas', 'output', 'template']
            ):
                continue

            ext = pfile.suffix[1:] if pfile.suffix else ""

            if name == 'datas':
                if ext != 'yaml':
                    continue

            else:
                keepthis = False

                for gext in flavours_exts:
                    if pfile.match(gext):
                        keepthis = True
                        break

                if not keepthis:
                    continue

            dest = TESTS_USECASES_DIR / fl / (pfile - usecase_dir)

            pfile.copy_to(dest)
