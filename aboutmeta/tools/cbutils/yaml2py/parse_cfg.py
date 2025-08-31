#!/usr/bin/env python3

from pathlib import Path
import              re
import              sys

from yaml import safe_load

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.core import *


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
TAG_FINAL_OPTIONAL = '*'
TAG_FINAL_POSTPROD = '+'

TAG_SEP_ALTERNATIVE = '|'
# TAG_SEP_CONJUNCTION = ','

TAG_MAGIC_CHAR = '.'

PATTERN_LEGAL_NAME = re.compile(r"[a-zA-Z_]+(\.[a-zA-Z_]+)*")
PATTERN_LIST_OF    = re.compile(r"list\s*\(\s*(.*?)\s*\)")

MSG_ERROR_BAD_VALIDATION = "Bad contrib. validation"


# ------------ #
# -- TYPING -- #
# ------------ #

type NestedYAMLDic     = dict[str, str | list[str] | NestedYAMLDic]
type NestedDictBoolStr = dict[str, bool | str | NestedDictBoolStr]


# ------------------- #
# -- YAML ANALYSIS -- #
# ------------------- #

###
# prototype::
#     key : XXX
#
#     :return: ''(name, is_required)'' XXX
###
def get_name_n_isrequired(key: str) -> tuple[str, bool]:
    if key[-1] == TAG_FINAL_OPTIONAL:
        is_required = False
        name        = key[:-1]

    else:
        is_required = True
        name        = key

    name = name.strip()

    return name, is_required


# -------------------------- #
# -- YAML DICT TO PY DICT -- #
# -------------------------- #


###
# prototype::
#     file : XXX
#
#     :return: XXX
###
def digested_yaml_specs(file: Path) -> NestedDictBoolStr:
    specs = safe_load(file.read_text())

# Extra tags?
    extradata = dict()

    for k in specs:
        if PATTERN_SPECIAL_TAGS_SPECS.fullmatch(k):
            if not k in SPECIAL_TAGS_SPECS:
                log_raise_error(
                    context = MSG_ERROR_BAD_VALIDATION,
                    desc    = (
                        f"Illegal special key '{k}' in '{file}'."
                    ),
                    exception = ValueError,
                )

            extradata[k] = specs[k]

    for k in extradata:
        del specs[k]

    extradata[SPECIAL_TAG_FILE] = file

# Let us work recursively, starting with a fake initial key.
    specs = build_pyspecs(
        {_TAG_FAKE: specs},
        extradata,
    )

    specs = specs[_TAG_FAKE]

# Not need to know requirement value at the very first level.
    del specs[TAG_SPECS_REQUIRED]

# Nothing left to do!
    return specs


###
# prototype::
#     specs    : XXX
#     extradata: XXX
#
#     :return: XXX
###
def build_pyspecs(
    specs    : NestedYAMLDic,
    extradata: dict[str, str]
) -> NestedDictBoolStr:
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


###
# prototype::
#     file : XXX
#
#     :return: XXX
###
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

###
# prototype::
#     file : XXX
#
#     :return: XXX
###
def split_key_val(
    key      : str,
    val      : str | list[str] | NestedYAMLDic,
    extradata: dict[str, str],
):
    TODO
# List used.
    if isinstance(val, list):
        raise_validation_error(
            key        = key,
            yfile_name = extradata[TAG_FILE],
            desc       = "value can't be a dict.",
        )
        log_raise_error(
            context = MSG_ERROR_BAD_VALIDATION,
            desc    = (
                f"Illegal value for the key '{k}' in "
                f"'{extradata[TAG_FILE]}'."
            ),
            exception = ValueError,
        )

# Multiple keys used.
    if isinstance(val, dict):
        raise_validation_error(
            key        = key,
            yfile_name = extradata[TAG_FILE],
            desc       = "value can't be a dict.",
        )
        log_raise_error(
            context = MSG_ERROR_BAD_VALIDATION,
            desc    = (
                f"Illegal special key '{k}' in '{file}'."
            ),
            exception = ValueError,
        )

# About the key(s).
    real_key, is_required = get_name_n_isrequired(key)

# Single key used.
    if not TAG_SEP_ALTERNATIVE in real_key:
        if TAG_SEP_ALTERNATIVE in val_not_list:
            raise_validation_error(
                key        = key,
                yfile_name = extradata[TAG_FILE],
                desc       = "different numbers of pipe.",
            )

        return is_required, [real_key], [val_not_list]



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







###
# prototype::
#     file : XXX
#
#     :return: XXX
###
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
        if val[-1] == TAG_FINAL_POSTPROD:
            use_post_prod = True
            val           = val[:-1].strip()

# Nothing left to do.
    return is_list_of, use_post_prod, val
