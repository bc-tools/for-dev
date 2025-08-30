#!/usr/bin/env python3

import re

from yaml import safe_load


# --------------- #
# -- CONSTANTS -- #
# --------------- #

_TAG_FAKE  = '.:fake:.'

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

# We are giving ourselves the option in the future to use special
# '__name__' for specific treatments in YAML specs.

SPECIAL_TAG_FILE = '__file__'

PATTERN_SPECIAL_TAGS_SPECS = re.compile(r'__[a-z]+__')

SPECIAL_TAGS_SPECS = []

# Standard features.
TAG_OPTIONAL   = '*'
TAG_ALT_SEP    = '|'
TAG_POST_PROD  = '+'
TAG_MAGIC_CHAR = '.'

PATTERN_LEGAL_NAME = re.compile(r"[a-zA-Z_]+(\.[a-zA-Z_]+)*")
PATTERN_LIST_OF    = re.compile(r"list\s*\(\s*(.*?)\s*\)")


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


# -------------------------- #
# -- YAML DICT TO PY DICT -- #
# -------------------------- #

def digested_specs(yaml_file):
    yfile_name = yaml_file.name
    specs      = safe_load(yaml_file.read_text())

# Extra tags?
    extradata = dict()

    for k in specs:
        if PATTERN_SPECIAL_TAGS_SPECS.fullmatch(k):
            if not k in SPECIAL_TAGS_SPECS:
                raise_validation_error(
                    key        = k,
                    yfile_name = yfile_name,
                    desc       = "illegal special key."
                )

            extradata[k] = specs[k]

    for k in extradata:
        del specs[k]

    extradata[SPECIAL_TAG_FILE] = yaml_file

# Let's work recursively with a fake dict.
    fake_specs = build_pyspecs(
        {_TAG_FAKE: specs},
        extradata,
    )

    specs = fake_specs[_TAG_FAKE]

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

        use_post_prod = last_parser if use_post_prod else ''

        this_specs = {
            TAG_SPECS_TYPE     : TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF  : is_list_of,
            TAG_SPECS_PARSER   : last_parser,
        }

        if is_list_of:
            this_specs[TAG_SPECS_MAPPER] = use_post_prod

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
    real_key, is_required = get_name_required(key)

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
