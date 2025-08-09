#!/usr/bin/env python3

# from pprint import pprint

from .common import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# We are giving ourselves the option in the future to use special
# ''__name__'' for specific treatments in YAML specs.

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
PATTERN_LIST_OF    = re.compile(r"list\(\s*(.*)\s*\)")

PY_TAGS = [
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


# -------------- #
# -- EASY LOG -- #
# -------------- #

def raise_validation_error(
    key,
    yfile_name,
    desc,
    xtra = ""
):
    desc = f"See ''{key}'' key in ''{yfile_name}'' file: {desc}"

    logging.error(
        log_title(
            TAG_BAD_VALIDATION,
            desc = desc
        )
    )

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

# Legal extra tags?
    extradata = dict()

    for k in specs:
        if PATTERN_SPECIAL_TAGS_SPECS.fullmatch(k):
            if not k in SPECIAL_TAGS_SPECS:
                raise ValueError(
                    f"illegal special key ''{k}'' in "
                    f"''specs/{yfile_name}'' file."
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
        is_list_of, use_post_prod, val = normalize_val(
            key,
            val,
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
            )

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


# ------------- #
# -- PY CODE -- #
# ------------- #

def build_block_pycodes(
    context,
    yaml_files,
    srcdir,
):
    codes_added = set()

    for yfile in yaml_files:
        codes_added.add(yfile.stem)

        logging.info(
            log_title(
                title = context,
                desc  = yfile.stem
            )
        )

        build_single_block_pycode(
            yaml_file = yfile,
            pyspecs = digested_specs(yfile)
        )



    return codes_added


def build_single_block_pycode(
    yaml_file,
    pyspecs
):
    from rich import print
    print(yaml_file)
    print(pyspecs)

    exit()
