#!/usr/bin/env python3

from typing import List

import                   logging
from rich.logging import RichHandler

from pathlib import Path
from yaml    import safe_load

from aboutmeta.data.boxplus import BoxPlus
from aboutmeta.data.license import License
from aboutmeta.specs        import *
from aboutmeta.style        import ALL_STYLES
from aboutmeta.tool.license import get_licence_text


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAG_STYLE_DEFAULT = 'default'


# --------------------- #
# -- LOGGING CONFIG. -- #
# --------------------- #

LOG_FILE = "aboutmeta.validate.log"

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


# -------------------------- #
# -- ABOUTMETA DATA CLASS -- #
# -------------------------- #

###
# The ''AMData'' class is responsible for orchestrating data
# extraction and validation.
###
class AMData:
###
# prototype::
#     style : this \arg corresponds to the syntax style used
#             by the path::''about.yaml'' file (for now, this
#             \arg is useless because there is only one style).
###
    def __init__(
        self,
        style = TAG_STYLE_DEFAULT
    ) -> None:
        self.style = style

###
# We define accessors (getters and setters) to add certain treatments
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
            raise ValueError(f"''{style}'' is not a style of parsers.")

        self._parsers = ALL_STYLES[style]
        self._style   = style


### TODO
# prototype::
#     yaml_file   : the path of the path::''about.yaml'' file analyzed.
#     auto_suffix : XXX
#
#     :action: XXX
###
    def build(
        self,
        yaml_file  : Path,
        auto_suffix: str = ""
    ) -> None:
        self._yaml_file_dir = yaml_file.parent
        self._auto_suffix   = f".{auto_suffix}"

        self.data = BoxPlus(
            self.__recu_parse(
                safe_load(yaml_file.read_text()),
                SPECS_PARSING
            )
        )

### TODO
# prototype::
#     data  : XXX
#     specs : XXX
#
#     :action: XXX
###
    def __recu_parse(
        self,
        data : BoxPlus,
        specs: dict
    ) -> dict:
        data_parsed = {}

# Illegal alternatives?
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

                if parser_name is None:
                    _parser = str

                else:
                    _parser = getattr(
                        self._parsers,
                        parser_name
                    )

                if parser_name == TAG_PARSER_PATH:
                    parser = lambda x: _parser(
                        self._yaml_file_dir,
                        x,
                        self._auto_suffix
                    )

                else:
                    parser = lambda x: _parser(x)

                if loc_specs[TAG_SPECS_LIST_OF]:
                    for i, d in enumerate(val):
                        val[i] = parser(val[i])

                    data_parsed[key] = val

                else:
                    data_parsed[key] = parser(val)

# Job done.
        return data_parsed

###
# prototype::
#     what  : a virtual path to access the license specified in the
#             analyzed path::‘'about.yaml’' file.
#     where : the folder where to add the file path::''LICENSE.txt''.
#             This folder is indicated using a textual path relative
#             to the folder containing the file path::‘'about.yaml’'.
#     erase : set to ''True'', this \arg allows to erase an existing
#             final file to build a new one.
#
#     :action: Create or update a path::''LICENSE.txt'' file in the
#              specified folder with the text of the selected license.
###
    def add_license(
        self,
        what : str,
        where: str,
        erase: bool = False
    ) -> None:
# Do we have a license?
        lic = self.data(what)

        if not isinstance(lic, License):
            raise ValueError(
                f"not a virtual path to a license: ''{what}''."
            )

# Text of the license.
        license_text = get_licence_text(lic.std)

# File for the license.
        license_file = self._yaml_file_dir

        for subfolder in where.split('/'):
            license_file /= subfolder

        license_file /= "LICENSE.txt"

# Can we erase an existing final file?
        if license_file.is_file() and not erase:
            raise IOError(
                f"the class {type(self).__name__} is not allowed "
                "to erase the LICENSE file:"
                "\n"
                f"{license_file}"
            )

# Missing folder for the license file?
        if not license_file.parent.is_dir():
            license_file.parent.mkdir(
                parents  = True,
                exist_ok = True
            )

# Everything looks good. Let's write the license text.
        license_file.touch()
        license_file.write_text(license_text)

###
# prototype::
#     what      : either ''None'' to validate evrything, or a
#                 virtual path to a block or data to be validated.
#                 In the case of a block, a recursive search for
#                 the data to be validated is performed automatically.
#     erase_log : set to ''True'', this \arg allows to erase an
#                 existing ''LOG_FILE'' file used to store errors.
#
#     :return: ''True'' if all data has been validated, and ''False''
#              if not.
#
#     :see: self.__recu_validate
#
# note::
#     The validation process is detailed in the terminal, but only
#     errors are recorded in the ''LOG_FILE'' file.
###
    def validate(
        self,
        what     : (str | None) = None,
        erase_log: bool = False
    ) -> bool:
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
        return self.__recu_validate(data) == 0

###
# prototype::
#     data : XXX
#
#     :return: CCCC
###
    def __recu_validate(
        self,
        data
    ) -> bool:
        nb_pbs = 0

# One dict?
        if isinstance(data, dict):
            for key, val in data.items():
                nb_pbs += self.__recu_validate(val)

# One list?
        elif isinstance(data, list):
            for val in data:
                nb_pbs += self.__recu_validate(val)

# One data to validate?
        elif hasattr(data, 'validate'):
            nb_pbs += data.validate()

        return nb_pbs








if __name__ == "__main__":
    readme_dir = Path(__file__).parent.parent.parent / "readme"
    filetest   = readme_dir / "about.yaml"

    xtrct = AMData()
    xtrct.build(filetest, auto_suffix = "md")

    for p in xtrct.data.toc:
        print(f"+ {p.relative_to(readme_dir)}")
