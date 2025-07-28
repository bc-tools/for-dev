#!/usr/bin/env python3

from typing import (
    Any,
    List
)

import                   logging
from rich.logging import RichHandler

from pathlib import Path

from yaml import safe_load

from aboutmeta.data.constants import *
from aboutmeta.data.specs     import *
from aboutmeta.style          import ALL_STYLES

from aboutmeta.data.boxplus   import BoxPlus
from aboutmeta.data.license   import License
from aboutmeta.data.tocpath   import TOCPath
from aboutmeta.tool.license   import get_licence_text


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAG_STYLE_DEFAULT = 'default'

SET_KEEP_ALL      = set(SPECS)
SET_KEEP_ONLY_TOC = set(["toc"])


# --------------------- #
# -- LOGGING CONFIG. -- #
# --------------------- #

LOG_FILE = "aboutmeta.log"

# Terminal settings.
#
# ''rich_tracebacks = True'' enables colorful, detailed tracebacks
# when unhandled exceptions occur, showing code context.
term_handler = RichHandler(rich_tracebacks = True)
term_handler.setLevel(logging.INFO)

# File settings.
file_handler = logging.FileHandler(
    LOG_FILE,
    mode = "a"
)
file_handler.setLevel(logging.ERROR)

file_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)
file_handler.setFormatter(file_formatter)

# Global settings.
logging.basicConfig(
# Resetting configurations
    force    = True,
# Lowest level for taking our levels into account.
    level    = logging.DEBUG,
    handlers = [
        term_handler,
        file_handler
    ],
)


# ------------------------------ #
# -- PRE ABOUTMETA DATA CLASS -- #
# ------------------------------ #

###
# The ''PreAMData'' class implements the main logic for orchestrating
# data extraction and validation.
#
# note::
#     Specific processes such as adding a license or post-productions
#     will be handled in the child class ''amdata.AMData''.
###
class PreAMData:
###
# prototype::
#     style : this \arg corresponds to the syntax style used by the
#             path::''about.yaml'' file (for now, this \arg is
#             useless because there is only one style).
###
    def __init__(
        self,
        style = TAG_STYLE_DEFAULT
    ) -> None:
        self.style = style

        self.at_least_one_validation = False

###
# We define accessors (getters and setters) to add some treatments
# to be performed when a style change occurs.
###
    @property
    def style(self) -> str:
        return self._style

    @style.setter
    def style(
        self,
        style: str
    ) -> None:
        if not style in ALL_STYLES:
            raise ValueError(f"unknown parser style ''{style}''.")

        self._parsers = ALL_STYLES[style]
        self._style   = style

###
# prototype::
#     yaml_file : the path of the path::''about.yaml'' file analyzed.
#     keep      : set of main blocks to analyze.
#
#     :action: build the ''BoxPlus'' version of the data found.
#
#     :see: self.__recu_parse.
###
    def build(
        self,
        yaml_file: Path,
        keep     : set[str] = SET_KEEP_ALL
    ) -> None:
        self._yaml_file_dir = yaml_file.parent

        full_data = {
            k: v
            for k, v in safe_load(yaml_file.read_text()).items()
            if k in keep
        }

        self.data = BoxPlus(
            self.__recu_parse(full_data, SPECS)
        )

###
# prototype::
#     data  : one piece of data (either a block, a list, or a final
#             data).
#     specs : "local" \specs corresponding to the data analyzed.
#
#     :action: validate the \yaml data, then build the corresponding
#              \python version.
###
    def __recu_parse(
        self,
        data : dict,
        specs: dict
    ) -> dict:
        data_parsed = {}

# Illegal alternatives?
        self.__no_alt_keys_together(data, specs)

# Let's parse...
        for key, val in data.items():
# Legal key?
            if not key in specs:
                raise KeyError(f"unknown key ''{key}''.")

            loc_specs = specs[key]

# Good kind of data?
            key_type = loc_specs[TAG_SPECS_TYPE]

            needed = ""

            match key_type:
                case "BLOCK":
                    if not isinstance(val, dict):
                        needed = "block"

                case "DATA":
                    if loc_specs[TAG_SPECS_LIST_OF]:
                        if not isinstance(val, list):
                            needed = "list of data"

                    elif not isinstance(val, str):
                        needed = "data"

            if needed:
                raise ValueError(
                    f"content of ''{key}'' must be a {needed}."
                )

# Block data needs a recursive work.
            if key_type == TAG_SPECS_BLOCK:
                data_parsed[key] = self.__recu_parse(
                    val,
                    loc_specs[TAG_SPECS_CONTENT]
                )

# List of data needs an iterative parsing.
            else:
                parser_name = loc_specs[TAG_SPECS_PARSER]

                if parser_name == TAG_PARSER_STR:
                    _parser = str

                else:
                    _parser = getattr(
                        self._parsers,
                        parser_name
                    )

                if parser_name == TAG_PARSER_TOCPATH:
                    parser = lambda x: _parser(
                        self._yaml_file_dir,
                        x
                    )

                else:
                    parser = lambda x: _parser(x)

                if loc_specs[TAG_SPECS_LIST_OF]:
                    for i, d in enumerate(val):
                        val[i] = parser(val[i])

                    if loc_specs[TAG_SPECS_POST_PROD]:
                        val = self.use_post_prod(key, val)

                    data_parsed[key] = val

                else:
                    data_parsed[key] = parser(val)

# Job done.
        return data_parsed

###
# prototype::
#     data  : one piece of data (either a block, a list, or a final
#             data).
#     specs : "local" \specs corresponding to the data analyzed.
#
#     :action: verification that two competing keys are not used
#              simultaneously.
###
    def __no_alt_keys_together(
        self,
        data : dict,
        specs: dict
    ) -> None:
        if specs[TAG_SPECS_ALT_ALL]:
            keys_set   = set(data.keys())
            to_analyze = keys_set.intersection(
                set(specs[TAG_SPECS_ALT_ALL])
            )

            if len(to_analyze) > 1:
                for no_alt in specs[TAG_SPECS_ALT_TUPLES]:
                    common_keys = keys_set.intersection(no_alt)

                    if len(common_keys) > 1:
                        common_keys = list(common_keys)
                        common_keys.sort()
                        common_keys = [f"''{k}''" for k in common_keys]
                        common_keys = ', '.join(common_keys)

                        raise ValueError(
                            f"just use on the keys {common_keys}."
                        )

###
# prototype::
#     key: a \yaml key.
#     val: the parsed "partial" \val.
#
#     :return: the final \val build by a post-production process.
#
# caution::
#     We use this pseudo-method instead of a single ''getattr'' in
#     order to eliminate the post-production process when formatting
#     an path::''about.yaml'' file.
###
    def use_post_prod(
        self,
        key: str,
        val: Any
    ) -> Any:
        return getattr(self, f"post_{key}")(val)

###
# prototype::
#     what      : either ''None'' to validate evrything, or a
#                 virtual path to a block or data to be validated.
#                 In the case of a block, a recursive search for
#                 the data to be validated is performed automatically.
#     erase_log : set to ''True'', this \arg allows to erase an
#                 existing ''LOG_FILE'' file used to store errors.
#
#     :return: the number of errors found.
#
#     :see: self.__recu_validate
#
#
# note::
#     The validation process is detailed in the terminal, but only
#     errors are recorded in the ''LOG_FILE'' file.
###
    def validate(
        self,
        what     : (str | None) = None,
        erase_log: bool = False
    ) -> int:
        self.at_least_one_validation = False

# Which data to validate?
        if what is None:
            data = self.data

        else:
            data = self.data(what)

# Do we have to erase the log file?
        if erase_log:
            Path(LOG_FILE).touch()
            Path(LOG_FILE).write_text("")

# Let's delegate the work to a recursive company.
        return self.__recu_validate(data)

###
# prototype::
#     data : one piece of data (either a ''BoxPlus'', a list, or a
#            final data).
#
#     :return: the \nb of \pbs found during the validation of ''data''.
###
    def __recu_validate(
        self,
        data: Any
    ) -> int:
        nb_pbs = 0

# One dict?
        if isinstance(data, BoxPlus):
            for key, val in data.items():
                nb_pbs += self.__recu_validate(val)

# One list?
        elif isinstance(data, list):
            for val in data:
                nb_pbs += self.__recu_validate(val)

# One data to validate?
        elif hasattr(data, 'validate'):
            self.at_least_one_validation = True

            nb_pbs += data.validate()

        return nb_pbs
