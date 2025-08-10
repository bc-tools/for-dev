#!/usr/bin/env python3

# from rich import print

from utilities.cnp_code import *


# --------------- #
# -- TEMPLATES -- #
# --------------- #

TEMPL_FLAVOURS = f"""
{TEMPL_CODE_HEADER}

from aboutmeta.specs.constants import *


# --------------- #
# -- ALL SPECS -- #
# --------------- #

SPECS = {{specs_code}}
""".strip() + '\n'


# ------------- #
# -- PY CODE -- #
# ------------- #

def build_flavour_pycodes(
    context,
    srcdir,
    yaml_files,
    projdir,
    testsdir,
):
    logging.info(
       f"{context.upper()} - Validating YAML contribs."
    )

# All the existent main blocks.
    main_blocks = set(
        f.stem
        for f in (srcdir.parent / "block").glob("*.py")
        if f.name != INIT_FILE
    )

# Specs validations.
    codes_added = set()

    specs        = dict()
    flavour_tags = dict()

    for yfile in yaml_files:
        logging.info(
            log_title(
                title = context,
                desc  = yfile.name
            )
        )

        block_list = safe_load(yfile.read_text())

        if not isinstance(block_list, list):
            raise_validation_error(
                key        = '',
                yfile_name = yfile.name,
                desc       = "a list of main block names is expected."
            )

# Do we have know main block names?
        pre_locspecs = get_prespecs(block_list)

        if not (set(pre_locspecs) <= main_blocks):
            unknwon_names = sorted(
                list(set(pre_locspecs) - main_blocks)
            )

            plurials = '' if len(unknwon_names) == 1 else 's'

            unknwon_names = [''] + unknwon_names
            unknwon_names = '\n  + '.join(unknwon_names)

            raise_validation_error(
                key        = '',
                yfile_name = yfile_name,
                desc       = f"unknown main block name{plurials}.",
                xtra       = unknwon_names
            )

# No problem.
        locspecs = {
            TAG_SPECS_OPTIONAL: set(),
            TAG_SPECS_REQUIRED: set(),
        }

        for block_name, is_required in pre_locspecs.items():
            kind = TAG_SPECS_REQUIRED if is_required else TAG_SPECS_OPTIONAL

            locspecs[kind].add(block_name)

        specs[yfile.stem] = locspecs

        flavour_pyname = get_pyname(yfile.stem)

        codes_added.add(flavour_pyname)

        flavour_tags[f"TAG_FLAVOUR_{flavour_pyname.upper()}"] = yfile.stem

    if specs:
# Let's build the code.
        logging.info(message_creation_update(context))

        logging.info(
            log_title(
                title = context,
                desc  = FLAVOURS_FILE
            )
        )

        flavour_tags_code = '\n'.join([
            f"{p} = {y!r}"
            for p, y in flavour_tags.items()
        ])

        allvars = copy(globals())

        specs_code = code_with_metatags(
            allvars  = allvars,
            metavars = get_metatags(allvars),
            code     = repr(specs)
        )

        for p, y in flavour_tags.items():
            specs_code = specs_code.replace(f"{y!r}:", f"{p}:")

        code = TEMPL_FLAVOURS.format(
            specs_code = specs_code,
        )

        add_black_pyfile(
            code,
            srcdir.parent / FLAVOURS_FILE
        )

# Add new tags in 'contants.py' file.
        append_black_pyfile(
            flavour_tags_code,
            srcdir.parent / CONSTANTS_FILE
        )

# Checking tests?
        missing_unit_tests(
            context,
            codes_added,
            projdir,
            testsdir,
        )

def get_prespecs(block_list):
    specs = {}

    for block_name in block_list:
        block_name, is_required = get_name_required(block_name)

        specs[block_name] = is_required

    return specs
