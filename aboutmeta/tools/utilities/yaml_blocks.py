#!/usr/bin/env python3

# from pprint import pprint

from utilities.cnp_code import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# We are giving ourselves the option in the future to use special
# '__name__' for specific treatments in YAML specs.

PATTERN_SPECIAL_TAGS_SPECS = re.compile(r'__[a-z]+__')

SPECIAL_TAGS_SPECS = []


# Standard features.
TAG_BAD_VALIDATION = "bad validation"
TAG_FILE           = "file"

TAG_ALT_SEP    = '|'
TAG_POST_PROD  = '+'
TAG_OPTIONAL   = '*'
TAG_MAGIC_CHAR = '.'

PATTERN_LEGAL_NAME = re.compile(r"[a-zA-Z_]+(\.[a-zA-Z_]+)*")
PATTERN_LIST_OF    = re.compile(r"list\s*\(\s*(.*?)\s*\)")

META_TAGS = [
    TAG_SPECS_ALT_ALL   := "__ALT_ALL__",
    TAG_SPECS_ALT_TUPLES:= "__ALT_TUPLES__",
    TAG_SPECS_BLOCK     := "__BLOCK__",
    TAG_SPECS_CONTENT   := "__CONTENT__",
    TAG_SPECS_DATA      := "__DATA__",
    TAG_SPECS_LIST_OF   := "__LIST_OF__",
    TAG_SPECS_POST_PROD := "__POST-PROD__",
    TAG_SPECS_PARSER    := "__PARSER__",
    TAG_SPECS_REQUIRED  := "__REQUIRED__",
    TAG_SPECS_TYPE      := "__TYPE__",
]

# Python codes.

ARG_TAGS = [
    TAG_ARG_AMDATA_CLS:= "amdata_cls",
    TAG_ARG_DATA      := "data",
    TAG_ARG_DATA_LIST := "data_list",
    TAG_ARG_PARENT    := "parent",
]

PARSING_FOLDERS = [
    PARSER_SUBDIR:= "parser",
    MAPPER_SUBDIR:= "mapper",
]

PATTERN_PARSER_IN_PYSPECS = re.compile(r"TAG_SPECS_PARSER: ('([a-zA-Z_]+)')")


# --------------- #
# -- TEMPLATES -- #
# --------------- #

TEMPL_CSTS = f"""
{TEMPL_BLACK_HEADER}

{{imports_code}}


# --------------- #
# -- META TAGS -- #
# --------------- #

{{metatags_code}}
""".strip() + '\n'

TEMPL_SIGNS = f"""
{TEMPL_BLACK_HEADER}

from aboutmeta.block.{TAG_CONSTANTS} import *


# ---------------- #
# -- SIGNATURES -- #
# ---------------- #

SIGNATURES = {{signs_dict_code}}
""".strip() + '\n'


TEMPL_BLOCK = f"""
{TEMPL_BLACK_HEADER}

from aboutmeta.block.{TAG_CONSTANTS} import *


# ----------- #
# -- SPECS -- #
# ----------- #

SPECS = {{specs_dict_code}}
""".strip() + '\n'


# -------------- #
# -- EASY LOG -- #
# -------------- #

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


# --------------- #
# -- KEY / VAL -- #
# --------------- #

def normalize_val(
    key,
    val,
    extradata
):
    use_post_prod = False

# YAML list used.
    is_list_of = (isinstance(val, list))

    if is_list_of:
        if len(val) != 1:
            raise_validation_error(
                key        = key,
                yfile_name = extradata[TAG_FILE],
                desc       = "not a single element list value.",
            )

        val = val[0]

# Use of list(...)?
    if isinstance(val, str):
        match = PATTERN_LIST_OF.fullmatch(val)

        if match:
            is_list_of = True
            val        = match.group(1)

# Post prod?
        if val[-1] == TAG_POST_PROD:
            use_post_prod = True
            val           = val[:-1].strip()

# Nothing left to do.
    return is_list_of, use_post_prod, val


def split_key_val(
    key,
    val_not_list,
    extradata
):
# About the key(s).
    if key[-1] == TAG_OPTIONAL:
        is_required = False
        real_key    = key[:-1].strip()

    else:
        is_required = True
        real_key    = key

# Single key used.
    if not TAG_ALT_SEP in real_key:
        if TAG_ALT_SEP in val_not_list:
            raise_validation_error(
                key        = key,
                yfile_name = extradata[TAG_FILE],
                desc       = "different numbers of pipe.",
            )

        return is_required, [real_key], [val_not_list]

# Multiple keys used.
    if isinstance(val_not_list, dict):
        raise_validation_error(
            key        = key,
            yfile_name = extradata[TAG_FILE],
            desc       = "value can't be a dict.",
        )

# Let's split together.
    splitted_keys = [k.strip() for k in real_key.split('|')]
    splitted_vals = [v.strip() for v in val_not_list.split('|')]

    if len(splitted_keys) != len(splitted_vals):
        raise_validation_error(
            key        = key,
            yfile_name = extradata[TAG_FILE],
            desc       = "different numbers of pipe.",
        )

    return is_required, splitted_keys, splitted_vals


# -------------------------- #
# -- YAML DICT TO PY DICT -- #
# -------------------------- #

def digested_specs(yaml_file):
    yfile_name = yaml_file.name

    specs = safe_load(yaml_file.read_text())

# Extra tags?
    extradata = dict()

    for k in specs:
        if PATTERN_SPECIAL_TAGS_SPECS.fullmatch(k):
            if not k in SPECIAL_TAGS_SPECS:
                raise ValueError(
                    f"illegal special key '{k}' in "
                    f"'specs/{yfile_name}' file."
                )

            extradata[k] = specs[k]

    for k in extradata:
        del specs[k]

    extradata[TAG_FILE] = yfile_name

# Let's work recursively wwith a fake dict.
    fake_specs = build_pyspecs(
        {yaml_file.stem: specs},
        extradata,
    )

    specs = fake_specs[yaml_file.stem]

    del specs[TAG_SPECS_REQUIRED]

    return specs


def build_pyspecs(specs, extradata):
    pyspecs = {
        TAG_SPECS_ALT_ALL   : [],
        TAG_SPECS_ALT_TUPLES: [],
    }

# Recursive analysis.
    last_parser = None

    for key, val in specs.items():
        (
            is_required,
            splitted_keys,
            splitted_vals
        ) = split_key_val(
            key,
            val,
            extradata
        )

        if len(splitted_keys) > 1:
            pyspecs[TAG_SPECS_ALT_ALL].extend(splitted_keys)

            pyspecs[TAG_SPECS_ALT_TUPLES].append(tuple(splitted_keys))

        for k, v in zip(splitted_keys, splitted_vals):
            is_list_of, use_post_prod, v = normalize_val(
                k,
                v,
                extradata
            )

            if (
                use_post_prod
                and
                not is_list_of
            ):
                raise_validation_error(
                    key        = key,
                    yfile_name = extradata[TAG_FILE],
                    desc       = "post prod only for lists.",
                    xtra       = f"See the value of '{k}'.",
                )

            thispsec, last_parser = build_single_pyspec(
                k,
                v,
                is_list_of,
                use_post_prod,
                extradata,
                last_parser
            )

            thispsec[TAG_SPECS_REQUIRED] = is_required

            pyspecs[k] = thispsec

# Alternatives?
    if pyspecs[TAG_SPECS_ALT_ALL]:
        pyspecs[TAG_SPECS_ALT_ALL] = tuple(
            sorted(pyspecs[TAG_SPECS_ALT_ALL])
        )

        pyspecs[TAG_SPECS_ALT_TUPLES] = tuple(
            sorted(pyspecs[TAG_SPECS_ALT_TUPLES])
        )

    else:
        pyspecs[TAG_SPECS_ALT_ALL] = None

        del pyspecs[TAG_SPECS_ALT_TUPLES]

# Nothing left to do.
    return pyspecs


def build_single_pyspec(
    key,
    val_not_list,
    is_list_of,
    use_post_prod,
    extradata,
    last_parser
):
# A parser.
    if isinstance(val_not_list, str):
        if val_not_list == TAG_MAGIC_CHAR:
            if last_parser is None:
                raise_validation_error(
                    key        = key,
                    yfile_name = extradata[TAG_FILE],
                    desc       = (
                        "illegal use of the '.' alias "
                        "(no parser used at this time)"
                    ),
                )

            val_not_list = last_parser

        last_parser = val_not_list

        this_specs = {
            TAG_SPECS_TYPE     : TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF  : is_list_of,
            TAG_SPECS_PARSER   : last_parser,
            TAG_SPECS_POST_PROD: use_post_prod,
        }

# A sub block.
    else:
        last_parser = None

        this_specs = {
            TAG_SPECS_TYPE   : TAG_SPECS_BLOCK,
            TAG_SPECS_CONTENT: build_pyspecs(
                val_not_list,
                extradata,
            )
        }


    return this_specs, last_parser


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

        if parser == "str":
            return

        if parser not in parsing_tools[PARSER_SUBDIR]:
            raise_validation_error(
                key        = key,
                yfile_name = yaml_file_name,
                desc       = f"unknown parser '{parser}'.",
            )

        if (
            pyspecs[TAG_SPECS_POST_PROD]
            and
            parser not in parsing_tools[MAPPER_SUBDIR]
        ):
            raise_validation_error(
                key        = key,
                yfile_name = yaml_file_name,
                desc       = f"no mapper for '{parser}'.",
            )

# Recursive analysis.
    else:
        for k, v in pyspecs[TAG_SPECS_CONTENT].items():
            if k[:2] == '__':
                continue

            validate_pyspecs(
                k,
                yaml_file_name,
                parsing_tools,
                v,
            )


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

    specs = {}

    for yfile in yaml_files:
        yfile_stem = yfile.stem

        if yfile_stem in ILLEGAL_MAIN_BLOCK_NAMES:
            raise_validation_error(
                '',
                yfile.name,
                "illegal name for a main block."
            )

        logging.info(
            log_title(
                title = context,
                desc  = yfile.name
            )
        )

        pyspecs = digested_specs(yfile)

        validate_pyspecs(
            key            = '',
            yaml_file_name = yfile.name,
            parsing_tools  = parsing_tools,
            pyspecs        = pyspecs,
        )

        specs[f"{yfile_stem}.py"] = pyspecs

        codes_added.add(yfile_stem)

    if codes_added:
# Let's build Python codes.
        logging.info(message_creation_update(context))

        add_missing_dir(srcdir)

# Creation/update ''constants.py'' & ''signatures.py'' files.
        add_csts_file(
            parsing_tools,
            srcdir,
        )

# Creation/update block Python files.
        for pfile, specs in specs.items():
            logging.info(f"{context.upper()} - {pfile}")

            add_block_pyfile(
                srcdir / pfile,
                specs,
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

# Tests validations.


def get_metatags(vals = META_TAGS):
    allvars = copy(globals())

    return [
        vname
        for vname in allvars
        if globals()[vname] in vals
    ]


def add_csts_file(
    parsing_tools,
    srcdir,
):
    proj_srcdir = srcdir.parent

# Specific tags.
    metatags_code = [
        f"{vname} = {globals()[vname]!r}"
        for vname in get_metatags()
    ]

    metatags_code.append('')

    metatags_code += [
        f"{vname} = {globals()[vname]!r}"
        for vname in get_metatags(ARG_TAGS)
    ]

# Easy access to all parsers and mappers.
    imports_code = []
    signs_dict   = {}

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
                f"from aboutmeta.{module}.{name} import {fcname} as {alias_func}"
            )

            pyfile = proj_srcdir / kind / f"{name}.py"

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

    signs_dict_code = repr(signs_dict)

    for vname in get_metatags(ARG_TAGS):
        signs_dict_code = signs_dict_code.replace(
            f"{globals()[vname]!r}",
            vname
        )

# ''constants.py'' file.
    code = TEMPL_CSTS.format(
        imports_code      = '\n'.join(imports_code),
        metatags_code     = '\n'.join(metatags_code),
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


def add_block_pyfile(
    pfile,
    specs,
):
    specs_dict_code = repr(specs)

    code = TEMPL_BLOCK.format(
        specs_dict_code = specs_dict_code,
    )

    for vname in get_metatags():
        code = code.replace(f"{globals()[vname]!r}", vname)

    code = code.replace(
        "TAG_SPECS_PARSER: 'str'",
        "TAG_SPECS_PARSER: None",
    )

    code = PATTERN_PARSER_IN_PYSPECS.sub(
        lambda m: f"TAG_SPECS_PARSER: {m.group(2)}_parse",
        code
    )

    add_black_pyfile(code, pfile)
