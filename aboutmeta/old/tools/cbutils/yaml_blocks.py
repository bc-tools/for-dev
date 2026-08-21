#!/usr/bin/env python3

import re


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# For Python code translations.
ARG_TAGS = [
    TAG_ARG_AMDATA_CLS:= "amdata_cls",
    TAG_ARG_DATA      := "data",
    TAG_ARG_DATA_LIST := "data_list",
]

PARSING_FOLDERS = [
    PARSER_SUBDIR:= "parser",
    MAPPER_SUBDIR:= "mapper",
]

PATTERN_PARSER_IN_PYSPECS = re.compile(r"TAG_SPECS_PARSER: ('([a-zA-Z_]+)')")

PATTERN_MAPPER_IN_PYSPECS = re.compile(r"TAG_SPECS_MAPPER: ('([a-zA-Z_]+)')")


# --------------- #
# -- TEMPLATES -- #
# --------------- #

TEMPL_CSTS_BLOCK = f"""
{TEMPL_CODE_HEADER}

{{imports_code}}


# ---------- #
# -- TAGS -- #
# ---------- #

{{tags_code}}
""".strip() + '\n'

TEMPL_SIGNS = f"""
{TEMPL_CODE_HEADER}

from aboutmeta.specs.{TAG_CONSTANTS} import *


# ---------------- #
# -- SIGNATURES -- #
# ---------------- #

SPECS = {{signs_dict_code}}
""".strip() + '\n'


TEMPL_BLOCK = f"""
{TEMPL_CODE_HEADER}

from aboutmeta.specs.{TAG_CONSTANTS} import *


# ----------- #
# -- SPECS -- #
# ----------- #

SPECS = {{specs_dict_code}}
""".strip() + '\n'


# -------------------------- #
# -- YAML DICT TO PY DICT -- #
# -------------------------- #



# -------------------------------- #
# -- VALIDATE PARSERS & MAPPERS -- #
# -------------------------------- #

def get_all_parsing_tools(poject_srcdir):
    parsing_tools = {}

    for kind in PARSING_FOLDERS:
        parsing_tools[kind] = sorted([
            p.stem
            for p in (poject_srcdir / kind).glob("*.py")
            if p.name != INIT_FILE
        ])

    return parsing_tools


def validate_pyspecs(
    key,
    yaml_file_name,
    parsing_tools,
    pyspecs,
):
# Data.
    if pyspecs[TAG_SPECS_TYPE] == TAG_SPECS_DATA:
        parser = pyspecs[TAG_SPECS_PARSER]

        all_keys = set([key]) if key else set()

        if parser == "str":
            return all_keys

        if parser not in parsing_tools[PARSER_SUBDIR]:
            raise_validation_error(
                key        = key,
                yfile_name = yaml_file_name,
                desc       = f"unknown parser '{parser}'.",
            )

        if (
            pyspecs[TAG_SPECS_LIST_OF]
            and
            pyspecs[TAG_SPECS_MAPPER]
            and
            parser not in parsing_tools[MAPPER_SUBDIR]
        ):
            raise_validation_error(
                key        = key,
                yfile_name = yaml_file_name,
                desc       = f"no mapper for '{parser}'.",
            )

        return all_keys

# Recursive analysis.
    else:
        all_keys = set()

        for k, v in pyspecs[TAG_SPECS_CONTENT].items():
            if k[:2] == '__':
                continue

            all_keys = all_keys.union(
                validate_pyspecs(
                    k,
                    yaml_file_name,
                    parsing_tools,
                    v,
                )
            )

            all_keys.add(k)

# Keys will be used for tags.
        return all_keys



# ------------- #
# -- PY CODE -- #
# ------------- #

def build_block_pycodes(
    context,
    srcdir,
    yaml_files,
    projdir,
    testsdir,
):
    logging.info(
       f"{context.upper()} - Validating YAML contribs."
    )

# All the existent parsing tools.
    parsing_tools = get_all_parsing_tools(srcdir.parent)

# Specs validations.
    codes_added = set()
    all_keys    = set()
    specs       = {}

    for yfile in yaml_files:
        logging.info(
            log_title(
                title = context,
                desc  = yfile.name
            )
        )

        pyspecs = digested_specs(yfile)

        all_keys.add(yfile.stem)

        all_keys = all_keys.union(
            validate_pyspecs(
                key            = '',
                yaml_file_name = yfile.name,
                parsing_tools  = parsing_tools,
                pyspecs        = pyspecs,
            )
        )

        specs[f"{yfile.stem}.py"] = pyspecs

        codes_added.add(yfile.stem)

    if codes_added:
# Let's build Python codes.
        logging.info(message_creation_update(context))

        add_missing_dir(srcdir)

# Creation/update ''constants.py'' & ''signatures.py'' files.
        add_csts_files(
            parsing_tools,
            srcdir.parent,
            all_keys,
        )

# Creation/update block Python files.
        for pfile, specs in specs.items():
            logging.info(f"{context.upper()} - {pfile}")

            add_block_pyfile(
                srcdir / pfile,
                specs,
                all_keys
            )

# Nothing left expect the possible addition of an ''__init__.py'' file.
        add_missing_init(srcdir)

# Checking tests?
        missing_unit_tests(
            context,
            codes_added,
            projdir,
            testsdir,
        )

# Nothing left to do.
    return codes_added


def add_csts_files(
    parsing_tools,
    srcdir,
    all_keys,
):
    proj_srcdir = srcdir.parent

    _allvars = copy(globals())
    allvars  = {
        k: v
        for k, v in _allvars.items()
        if k[:4] == "TAG_"
    }

# Specific tags.
    tags_code = [
        f"{vname} = {allvars[vname]!r}"
        for vname in get_metatags(allvars)
    ]

    tags_code.append('')

    tags_code += [
        f"{vname} = {allvars[vname]!r}"
        for vname in get_metatags(allvars, ARG_TAGS)
    ]

    tags_code.append('')

    tags_code += [
        f"TAG_KEY_{k.upper()} = {k!r}"
        for k in sorted(list(all_keys))
    ]

# Easy access to all parsers and mappers.
    imports_code = []
    signs_dict   = dict()

    for kind, names in parsing_tools.items():
        module = kind

        if kind == PARSER_SUBDIR:
            fcname = alias = "parse"

        else:
            alias  = "map"
            fcname = "map_list"

        for name in names:
            alias_func = f"{name}_{alias}"

            imports_code.append(
                f"from aboutmeta.specs.{module}.{name} import {fcname} as {alias_func}"
            )

            pyfile = proj_srcdir / TAG_SPECS / kind / f"{name}.py"

            signature = get_parse_signature(
                file      = pyfile,
                func_name = fcname
            )

            for a in signature:
                if not a in ARG_TAGS:
                    raise_validation_error(
                        '',
                        pyfile.relative_to(proj_srcdir),
                        f"illegal argument '{a}' for '{fcname}'."
                    )

            signs_dict[alias_func] = signature

    signs_dict_code = code_with_metatags(
        allvars  = allvars,
        metavars = get_metatags(allvars, ARG_TAGS),
        code     = repr(signs_dict)
    )

# ''constants.py'' file.
    code = TEMPL_CSTS_BLOCK.format(
        imports_code = '\n'.join(imports_code),
        tags_code    = '\n'.join(tags_code),
    )

    add_black_pyfile(
        code,
        srcdir / CONSTANTS_FILE
    )

# ''signatures.py'' file.
    code = TEMPL_SIGNS.format(
        signs_dict_code = signs_dict_code,
    )

    add_black_pyfile(
        code,
        srcdir / SIGNS_FILE
    )

# Nothing left expect the possible addition of an ''__init__.py'' file.
    add_missing_init(srcdir)


def add_block_pyfile(
    pfile,
    specs,
    all_keys
):
    allvars         = copy(globals())

    specs_dict_code = repr(specs)

    code = TEMPL_BLOCK.format(
        specs_dict_code = specs_dict_code,
    )

    for vname in get_metatags(allvars):
        code = code.replace(f"{allvars[vname]!r}", vname)

    for old, new in [
        (
            "TAG_SPECS_PARSER: 'str'",
            "TAG_SPECS_PARSER: None",
        ),
        (
            "TAG_SPECS_MAPPER: ''",
            "TAG_SPECS_MAPPER: None",
        ),
    ]:
        code = code.replace(old, new)

    code = PATTERN_PARSER_IN_PYSPECS.sub(
        lambda m: f"TAG_SPECS_PARSER: {m.group(2)}_parse",
        code
    )

    code = PATTERN_MAPPER_IN_PYSPECS.sub(
        lambda m: f"TAG_SPECS_MAPPER: {m.group(2)}_map",
        code
    )

    for k in all_keys:
        code = code.replace(f"'{k}'", f"TAG_KEY_{k.upper()}")

    add_black_pyfile(code, pfile)
