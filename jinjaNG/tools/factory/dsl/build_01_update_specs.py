#!/usr/bin/env python3

from btools.B01 import *


# ! -- DEBUGGING -- ! #
# Clear the terminal.
# print("\033c", end="")

# from pprint import pprint
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


SPECS_SRC_FILE = PROJECT_DIR / 'src' / 'config' / 'jngflavours.py'

CONTRIB_DSL_DIR   = PROJECT_DIR / 'contribute' / 'api' / 'dsl'
SPECS_STATUS_YAML = THIS_DIR / 'flavours.yaml'

EXTRA_TOOLS_DIR = PROJECT_DIR / 'jngutils'


IMG_DIR  = 'images'
IMG_EXTS = ['png']


# ----------------------- #
# -- THE SPECS DEFINED -- #
# ----------------------- #

SPECS_STATUS = defaultdict(list)

specs_status = {}

for specfile in CONTRIB_DSL_DIR.rglob("*/*specs.yaml"):
    specdir = specfile.parent
    flavour = specdir.name

    specs_status_yaml = specdir / "status.yaml"

    if not specs_status_yaml.is_file():
        specs_status_yaml.touch()

        with specs_status_yaml.open(
            mode     = "w",
            encoding = "utf-8"
        ) as f:
            yaml_dump(DEFAULT_STATUS_CONTENT, f)

    with specs_status_yaml.open(
        mode     = "r",
        encoding = "utf-8"
    ) as f:
        specs_status[flavour]        = yaml_load(f)
        specs_status[flavour]['dir'] = specdir


# ---------------------------- #
# -- ALL THE SPECS ACCEPTED -- #
# ---------------------------- #

print(f"{TAB_1}* Specs of the accepted flavours.")

hard_specs_ok     = {}
some_extend_found = False

for flavour, specs in specs_status.items():
    if specs[TAG_STATUS] != STATUS_OK:
        continue

    with (specs['dir'] / 'specs.yaml').open(
        mode     = "r",
        encoding = "utf-8"
    ) as f:
        hardspec = yaml_load(f)

    if TAG_EXTEND in hardspec[TAG_ABOUT]:
        some_extend_found = True

    hard_specs_ok[flavour] = hardspec


# ---------------------------- #
# -- ALL THE SPECS ACCEPTED -- #
# ---------------------------- #

if some_extend_found:
    print(f"{TAB_1}* Taking care of ''extend''.")

    build_extended_flavours(hard_specs_ok)


# ------------------------------------------ #
# -- SPECS ACCEPTED / SPECS BEING UPDATED -- #
# ------------------------------------------ #

final_pycode   = []
ALL_FLAVOURS   = []
ASSOCIATED_EXT = {}
ALL_TOOLS      = []
not_ok         = defaultdict(list)


for flavour in sorted(specs_status):
    infos  = specs_status[flavour]
    status = infos['status']

    SPECS_STATUS[status].append(flavour)

# NOT OK.
    if status not in [STATUS_OK, STATUS_UPDATE]:
        if not infos['status'] in ALL_STATUS_TAGS:
            raise Exception(
                f"invalid status ''{infos['status']}'' "
                f"for the flavour ''{flavour}'' in "
                "the contributions."
            )

        not_ok[infos['status']].append(flavour)

        continue

# OK or UPDATING.
    print(f"{TAB_1}* {flavour}.")

    ALL_FLAVOURS.append(flavour)

# BEING UPDATED: we keep the source vecrsion.
    if status == STATUS_UPDATE:
        print(
            f"{TAB_2}+ Updating: use of the previous specs."
        )

        _, prevcode, _ = between(
            text = SPECS_SRC_FILE.read_text(
                encoding = 'utf-8'
            ),
            seps = [
                f'# -- {flavour.upper()}',
                 '}\n' # <-- Only one dict used!
            ],
        )

        prevcode = prevcode.split('\n')
        prevcode = prevcode[2:]
        prevcode.append('}')

        prevcode = "\n".join(prevcode)

        prevcode = f"""
{asciititle(flavour)}
{prevcode}
        """.strip()

        final_pycode += ['', prevcode]

        continue

# NEW SPECS, OR OLD ONES TO KEEP.
    print(f"{TAB_2}+ Analyzing the hard specs.")

    options = specs2options(hard_specs_ok[flavour])

    print(f"{TAB_2}+ Building the source code.")

    final_pycode += [
        '',
        build_src(flavour, options, ASSOCIATED_EXT),
    ]

    if options[TAG_UTILS]:
        print(f"{TAB_2}+ Referencing new tools.")

        ALL_TOOLS.append(flavour)


SPECS_STATUS[STATUS_OK] = ALL_FLAVOURS


# ------------------------------ #
# -- NO DUPLICATED EXTENSIONS -- #
# ------------------------------ #

_flavours = list(ASSOCIATED_EXT)

for i_ref, fl_ref in enumerate(_flavours):
    set_ref = ASSOCIATED_EXT[fl_ref]

    for fl_other in _flavours[i_ref + 1:]:
        inter = set_ref.intersection(ASSOCIATED_EXT[fl_other])

        if inter:
            plurial = "" if len(inter) == 1 else "s"

            inter = list(inter)
            inter.sort()
            inter = ', '.join(
                f'"{i}"'
                for i in inter
            )

            raise ValueError(
                f"same extension{plurial} for the flavours "
                f"''{fl_other}'' and ''{fl_ref}''. See:"
                 "\n"
                f"{inter}."
            )


# -------------------- #
# -- UPDATE PYFILES -- #
# -------------------- #

print(f"{TAB_1}* Updating the source code.")


ALL_FLAVOURS = [
    f"(FLAVOUR_{flvr.upper()}:= '{flvr}'),"
    for flvr in ALL_FLAVOURS
]


ALL_TAGS = []

final_pycode = '\n'.join(final_pycode)

myglobals = globals().copy()

for name, val in myglobals.items():
    if not name.startswith('TAG_'):
        continue

    pykey = f"'{val}':"

    if pykey in final_pycode:
        ALL_TAGS.append(
            f"({name}:= '{val}'),"
        )

        final_pycode = final_pycode.replace(pykey, f'{name}:')

ALL_TAGS.sort()


final_pycode = f"""
# Lines automatically build by the following file.
#
#     + ''{THIS_FILE_REL_SRC_PATH}''

ASSOCIATED_EXT = dict()
WITH_UTILS    = dict()
JINJA_TAGS    = dict()


# -------------- #
# -- ALL TAGS -- #
# -------------- #

ALL_TAGS = {ALL_TAGS}


# ------------------ #
# -- ALL FLAVOURS -- #
# ------------------ #

ALL_FLAVOURS = {ALL_FLAVOURS}

{final_pycode}
""".lstrip()

final_pycode = black.format_file_contents(
    final_pycode,
    fast = False,
    mode = black.FileMode()
).strip() + '\n'

for old, new in [
    ('"(FLAVOUR_', '(FLAVOUR_'),
    ('"(TAG_', '(TAG_'),
    ('),"', ')'),
]:
    final_pycode = final_pycode.replace(old, new)

with SPECS_SRC_FILE.open(
    encoding = 'utf8',
    mode     = 'w'
) as f:
    f.write(final_pycode)


# ------------------ #
# -- UPDATE TOOLS -- #
# ------------------ #

if ALL_TOOLS:
    print(f"{TAB_1}* Updating the tools.")

    for flavour in ALL_TOOLS:
        print(f"{TAB_2}* Tools for ''{flavour}''.")

        contrib_flavour_dir     = CONTRIB_DSL_DIR / flavour
        contrib_flavour_img_dir = contrib_flavour_dir / IMG_DIR

        xtratools_flavour_dir     = EXTRA_TOOLS_DIR / flavour
        xtratools_flavour_img_dir = xtratools_flavour_dir / IMG_DIR

# Images.
        imgs = [
            p
            for p in contrib_flavour_img_dir.glob("*")
            if p.ext in IMG_EXTS
        ]

        if imgs:
            if xtratools_flavour_img_dir.is_dir():
                xtratools_flavour_img_dir.remove()

            xtratools_flavour_img_dir.create('dir')

            for image in imgs:
                image.copy_to(
                    xtratools_flavour_img_dir / image.name,
                    safemode = False
                )

# Tools.
        for path in contrib_flavour_dir.glob("*"):
            if path.is_dir():
                continue

            if (
                path.stem.startswith('.')
                or
                path.name in ['status.yaml', 'specs.yaml']
            ):
                continue

            dest = xtratools_flavour_dir / path.name

            path.copy_to(
                dest,
                safemode = False
            )


# ---------------------------- #
# -- SPECS ON HOLD / NOT OK -- #
# ---------------------------- #

if not_ok:
    for status, about in [
        (STATUS_ON_HOLD, "Specs on hold."     ),
        (STATUS_KO     , "Specs rejected."),
    ]:
        flavours = not_ok[status]

        if not flavours:
            continue

        print(f"{TAB_1}* {about}")

        for fl in sorted(flavours):
            comment = specs_status[fl]['comment']
            comment = comment.strip()

            print(f"{TAB_2}+ ''{fl}'' --> {comment}")


# ----------------------- #
# -- SPECS STATUS YAML -- #
# ----------------------- #

print(f"{TAB_1}* Updating the status of specs (for other builders).")

# ! -- DEBUGGING -- ! #
# print(SPECS_STATUS)
# exit()
# ! -- DEBUGGING -- ! #

# Hack source for good indented YAML code:
#     * https://github.com/yaml/pyyaml/issues/234#issuecomment-765894586

SPECS_STATUS = {
    k: v
    for k, v in SPECS_STATUS.items()
}

with SPECS_STATUS_YAML.open(
    mode     = "w",
    encoding = "utf-8"
) as f:
    yaml_dump(
        data   = SPECS_STATUS,
        stream = f,
        Dumper = IndentDumper
    )
