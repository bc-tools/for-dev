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
TAG_POST_PROD  = "+"
TAG_OPTIONAL   = "*"
TAG_MAGIC_CHAR = "."

PATTERN_LEGAL_NAME = re.compile(r"[a-zA-Z_]+(\.[a-zA-Z_]+)*")
PATTERN_LIST_OF    = re.compile(r"list\((.*)\)")

PY_TAGS = [
    TAG_SPECS_ALT_ALL   := "ALT_ALL",
    TAG_SPECS_ALT_TUPLES:= "ALT_TUPLES",
    TAG_SPECS_BLOCK     := "BLOCK",
    TAG_SPECS_CONTENT   := "CONTENT",
    TAG_SPECS_DATA      := "DATA",
    TAG_SPECS_LIST_OF   := "LIST_OF",
    TAG_SPECS_POST_PROD := "POST-PROD",
    TAG_SPECS_PARSER    := "PARSER",
    TAG_SPECS_REQUIRED  := "REQUIRED",
    TAG_SPECS_TYPE      := "TYPE",
]

# ------------------ #
# -- YAML TO CODE -- #
# ------------------ #

def build_python_block_codes(
    context,
    yaml_files,
    srcdir,
):
    for yfile in yaml_files:
        logging.info(
            log_title(
                title = context,
                desc  = yfile.stem
            )
        )

        pyspecs = digested_specs(yfile)

        from pprint import pprint;pprint(pyspecs)
        exit()


def digested_specs(yaml_file):
    yfile_name = yaml_file.name

    specs = safe_load(yaml_file.read_text())

# Legal special tags?
    extradata = dict()

    for k in {yfile_name: specs}:
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

# Let's work recursively.
    return build_pyspecs(
        yfile_name,
        specs,
        extradata,
    )


def build_pyspecs(yfile_name, specs, extradata):
    pyspecs = {
        TAG_SPECS_ALT_ALL   : [],
        TAG_SPECS_ALT_TUPLES: [],
    }

# Recursive analysis.
    last_parser = None

    for key, val in specs.items():
        is_list_of, val = normalize_val(
            key,
            val,
            extradata
        )

        (
            key_kind,
            splitted_keys,
            splitted_vals
        ) = split_key_val(
            key,
            val,
            extradata
        )

        for k, v in zip(splitted_keys, splitted_vals):
            k, thispsec, last_parser = build_single_pyspec(
                k,
                v,
                extradata,
                last_parser
            )

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
        pyspecs[TAG_SPECS_ALT_ALL] = tuple()

        del pyspecs[TAG_SPECS_ALT_TUPLES]

# Nothing left to do.
    return pyspecs



def normalize_val(
    key,
    val,
    extradata
):
    is_list_of = (isinstance(val, list))

    if is_list_of:
        if len(val) != 1:
            raise_validation_error(
                key        = key,
                yfile_name = extradata[TAG_FILE],
                desc       = "not a single element list value.",
            )

        val = val[0]

    return is_list_of, val


def split_key_val(
    key,
    val_not_list,
    extradata
):
# About the key(s).
    real_key, key_kind = get_key_kind(key)

# Single key used.
    if not TAG_ALT_SEP in real_key:
        if TAG_ALT_SEP in val_not_list:
            raise_validation_error(
                key        = key,
                yfile_name = extradata[TAG_FILE],
                desc       = "different numbers of pipe.",
            )

        return key_kind, [real_key], [val_not_list]

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

    return key_kind, splitted_keys, splitted_vals



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


def get_key_kind(key):
# Key analysis.
    if key[-1] == TAG_OPTIONAL:
        is_required = False
        key         = key[:-1].strip()

    else:
        is_required = True

# Optional + Post-Prod is possible!
    if key[-1] == TAG_POST_PROD:
        post_prod = True
        key       = key[:-1].strip()

    else:
        post_prod = False

# Kind found.
    key_kind = {
        TAG_SPECS_REQUIRED : is_required,
        TAG_SPECS_POST_PROD: post_prod,
    }

# Job done.
    return key, key_kind



def build_single_pyspec(key, val, extradata, last_parser):
    this_specs = dict()


    print(key, val, extradata, last_parser,sep='\n')
    exit()


# Value analysis.
    if isinstance(val, str):
        # print(f"\n{key=} {val=} {last_parser=}")

        if TAG_MAGIC_CHAR in val:
            if last_parser is None:
                raise ValueError("illegal use of the ''.'' alias.")

            val = val.replace(
                TAG_MAGIC_CHAR,
                last_parser
            )

            # print(val, "???")

        is_list_of, parser = which_parser(val, extradata)

        last_parser = parser

        # print(parser, "????")

        this_specs |= {
            TAG_SPECS_TYPE     : TAG_SPECS_DATA,
            TAG_SPECS_LIST_OF  : is_list_of,
            TAG_SPECS_PARSER   : parser,
            TAG_SPECS_POST_PROD: post_prod,
        }


    else:
        last_parser = None

        this_specs[TAG_SPECS_TYPE]    = TAG_SPECS_BLOCK
        this_specs[TAG_SPECS_CONTENT] = build_pyspecs(
            yaml_file,
            val,
            extradata,
        )

    return key, this_specs, last_parser


def which_parser(kind, extradata):
    # global ALL_PARSERS_FOUND

    # if TAG_ABBREV in extradata:
    #     for oneabbrev, replacement in extradata[TAG_ABBREV].items():
    #         val = val.replace(f"\\{oneabbrev}", replacement)

    match = PATTERN_LIST_OF.fullmatch(kind)

    if not match:
        is_list_of = False

    else:
        is_list_of = True
        kind       = match.group(1)

    if not PATTERN_LEGAL_NAME.fullmatch(kind):
        if is_list_of:
            kind =f"list({kind})"

        raise ValueError(
            f"illegal type ''{kind}'' in "
            f"''specs/{extradata[TAG_FILE]}'' file."
        )

    # ALL_PARSERS_FOUND.add(kind)

    return is_list_of, kind
