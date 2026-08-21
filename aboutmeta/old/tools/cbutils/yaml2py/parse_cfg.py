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
TAG_SEP_SIMILAR     = ','

TAG_MAGIC_CHAR = '.'

PATTERN_LEGAL_NAME = re.compile(r"[a-zA-Z_]+(\.[a-zA-Z_]+)*")
PATTERN_LIST_OF    = re.compile(r"list\s*\(\s*(.*?)\s*\)")

MSG_ERROR_BAD_VALIDATION = "Bad contrib. validation"


# ------------ #
# -- TYPING -- #
# ------------ #

type NestedStrDic      = dict[str, str | NestedYAMLDic]
type NestedYAMLDic     = dict[str, str | list[str] | NestedYAMLDic]
type NestedDictBoolStr = dict[str, bool | str | NestedDictBoolStr]


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

# Unuseful requirement value at the very first level.
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

    for k, v in specs.items():
# Split regarding splitting characters.
        (
            keys, vals,
            is_required
        ) = split_keys_vals(
            k, v,
            extradata
        )

# Alternative keys used.
        if len(keys) > 1:
            pyspecs[TAG_SPECS_ALT_ALL].extend(keys)

            pyspecs[TAG_SPECS_ALT_TUPLES].append(tuple(keys))

# Normalisation of the keys and the values.
        for sk, sv in zip(keys, vals):
            sv, is_list_of, use_post_prod = normalize_val(
                sk, sv,
                extradata
            )

            if use_post_prod and not is_list_of:
                log_raise_error(
                    context = MSG_ERROR_BAD_VALIDATION,
                    desc    = (
                        f"Post prod only allowed for lists. See key "
                        f"'{k}' in '{extradata[SPECIAL_TAG_FILE]}'."
                    ),
                    exception = ValueError,
                )

            this_spec, last_parser = build_single_pyspec(
                sk, sv,
                is_list_of,
                use_post_prod,
                extradata,
                last_parser
            )

            this_spec[TAG_SPECS_REQUIRED] = is_required

            for conjkey in sk.split(','):
                conjkey = conjkey.strip()

                if not conjkey:
                    log_raise_error(
                        context = MSG_ERROR_BAD_VALIDATION,
                        desc    = (
                             "Illegal use of the conjunction operator ','. "
                            f"See YAML key '{sk}' in "
                            f"'{extradata[SPECIAL_TAG_FILE]}'."
                        ),
                        exception = ValueError,
                    )

                pyspecs[conjkey] = this_spec

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
    key          : str,
    val          : NestedStrDic,
    is_list_of   : bool,
    use_post_prod: bool,
    extradata    : dict[str, str],
    last_parser  : str
) -> NestedDictBoolStr:
# A parser.
    if isinstance(val, str):
        if val == TAG_MAGIC_CHAR:
            if last_parser is None:
                log_raise_error(
                    context = MSG_ERROR_BAD_VALIDATION,
                    desc    = (
                         "Illegal use of the '.' alias (no parser "
                        f"used at this time). See key '{key}' in "
                        f"'{extradata[SPECIAL_TAG_FILE]}'."
                    ),
                    exception = ValueError,
                )

            val = last_parser

        last_parser = val

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
                val,
                extradata,
            )
        }


    return this_specs, last_parser


# --------------- #
# -- KEY / VAL -- #
# --------------- #

###
# prototype::
#     key       :
#     val       :
#     extradata :
#
#     :return: XXX
###
def split_keys_vals(
    key      : str,
    val      : str | list[str] | NestedYAMLDic,
    extradata: dict[str, str],
):
# Let's split together.
    real_key, is_required = get_name_n_isrequired(key)

    splitted_keys = [
        k.strip()
        for k in real_key.split(TAG_SEP_ALTERNATIVE)
    ]

    if isinstance(val, str):
        splitted_vals = [
            v.strip()
            for v in val.split(TAG_SEP_ALTERNATIVE)
        ]

    else:
        splitted_vals = [val]

# We needthe same numbers of alternatives.
    if len(splitted_keys) != len(splitted_vals):
        if len(splitted_vals) !=1:
            log_raise_error(
                context = MSG_ERROR_BAD_VALIDATION,
                desc    = (
                    "Different number of pipes, or not one parser used. "
                    f"See key '{key}' in '{extradata[SPECIAL_TAG_FILE]}'."
                ),
                exception = ValueError,
            )

        splitted_vals = splitted_vals*len(splitted_keys)


# Nothing more to do here.
    return splitted_keys, splitted_vals, is_required


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


###
# prototype::
#     key       :
#     val       :
#     extradata :
#
#     :return: XXX
###
def normalize_val(
    key      : str,
    val      : str | list[str] | NestedYAMLDic,
    extradata: dict[str, str],
) -> tuple[NestedYAMLDic, bool, bool]:
    use_post_prod = False
    is_list_of    = (isinstance(val, list))

# YAML list used.
    if is_list_of:
        if len(val) != 1:
            log_raise_error(
                context = MSG_ERROR_BAD_VALIDATION,
                desc    = (
                    f"Key '{key}' needs a single element list value. "
                    f"See in '{extradata[SPECIAL_TAG_FILE]}'."
                ),
                exception = ValueError,
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
    return val, is_list_of, use_post_prod
