#!/usr/bin/env python3

from typing import List

from pathlib import Path
from yaml    import safe_load

from aboutmeta.data.boxplus import BoxPlus
from aboutmeta.data.license import License

# from aboutmeta.parser import (
#     date,
#     lang,
#     license,
#     person,
#     version,
# )

from aboutmeta.specs import *
from aboutmeta.style import ALL_STYLES

from aboutmeta.tool.license import get_licence_text





import logging
from rich.logging import RichHandler

LOG_FILE = "aboutmeta.validate.log"

# Console : afficher à partir de INFO
console_handler = RichHandler(rich_tracebacks=True)
console_handler.setLevel(logging.INFO)

# Fichier : enregistrer uniquement à partir de ERROR
file_handler = logging.FileHandler(LOG_FILE, mode="a")
file_handler.setLevel(logging.ERROR)

# Format pour fichier
file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(file_formatter)

# Config globale :
logging.basicConfig(
    level=logging.DEBUG,  # <-- Niveau global le plus bas pour tout capter
    handlers=[console_handler, file_handler],
    force=True,
)



# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAG_STYLE_DEFAULT = 'default'


# -------------------------- #
# -- ABOUTMETA DATA CLASS -- #
# -------------------------- #

###
# TODO
###
class AMData:
### TODO
# prototype::
#     style : XXX
###
    def __init__(
        self,
        style = TAG_STYLE_DEFAULT
    ) -> None:
        self.style = style

###
# TODO
###
    @property
    def style(self):
        return self._style

    @style.setter
    def style(
        self,
        style
    ):
        if not style in ALL_STYLES:
            raise ValueError(f"''{style}'' is not a style of parsers.")

        self._parsers = ALL_STYLES[style]
        self._style   = style


### TODO
# prototype::
#     yaml_file   : XXX
#     auto_suffix : XXX
#
#     :action: XXX
###
    def build(
        self,
        yaml_file,
        auto_suffix = ""
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
        data,
        specs
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

# Good kind of data?
            key_type = specs[key][TAG_SPECS_TYPE]

            needed = ""

            match key_type:
                case "BLOCK":
                    if not isinstance(val, dict):
                        needed = TAG_SPECS_BLOCK.lower()

                case "DATA":
                    if specs[key][TAG_SPECS_LIST_OF]:
                        if not isinstance(val, list):
                            needed = "list of data"

                    elif not isinstance(val, str):
                        needed = "a data"

            if needed:
                raise ValueError(
                    f"content of ''{key}'' must be a {needed}."
                )

# Block data needs a recursive work.
            if key_type == TAG_SPECS_BLOCK:
                data_parsed[key] = self.__recu_parse(
                    val,
                    specs[key][TAG_SPECS_CONTENT]
                )

# List of data needs an iterative parsing.
            else:
                parser_name = specs[key][TAG_SPECS_PARSER]

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

                if specs[key][TAG_SPECS_LIST_OF]:
                    for i, d in enumerate(val):
                        val[i] = parser(val[i])

                    data_parsed[key] = val

                else:
                    data_parsed[key] = parser(val)

# Job done.
        return data_parsed

###
# prototype::
#     license_path : a virtual path to access the license specified
#                    in the analyzed path::‘'about.yaml’' file.
#     dir_relpath  : a textual path relative to the folder containing
#                    the analyzed file path::‘'about.yaml’'.
#     erase        : set to ''True'', this \arg allows to erase an
#                    existing final file to build a new one.
#
#     :action: Create or update a path::''LICENSE.txt'' file in the
#              specified folder with the text of the selected license.
###
    def add_license(
        self,
        license_path : str,
        dir_relpath  : str,
        erase        : bool = False
    ) -> None:
        lic = self.data(license_path)

        if not isinstance(lic, License):
            raise ValueError(
                f"not a virtual path to a license: ''{license_path}''."
            )

        license_text = get_licence_text(lic.std)

        license_file = self._yaml_file_dir

        for subfolder in dir_relpath.split('/'):
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


        if not license_file.parent.is_dir():
            license_file.parent.mkdir(
                parents  = True,
                exist_ok = True
            )

        license_file.touch()
        license_file.write_text(license_text)

### TODO
# prototype::
#     :action: XXX
###
    def validate(
        self,
        data_path: (str | None) = None,
        erase_log: bool = False
    ) -> bool:
        if data_path is None:
            data = self.data

        else:
            data = self.data(data_path)

        if erase_log:
            Path(LOG_FILE).touch()
            Path(LOG_FILE).write_text("")

        return self.__recu_validate(data) == 0

### TODO
# prototype::
#     data  : XXX
#
#     :action: XXX
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
    from pprint import pprint

    filetest = Path(__file__).parent.parent.parent / "about.yaml"

    xtrct = AMData()
    xtrct.build(filetest, auto_suffix = "md")

    # xtrct.validate("project.author")

    pbs = xtrct.validate(
        erase_log = True
    )

    pprint(pbs)

    # xtrct.add_license(
    #     license_path = "project.licenses.manual",
    #     dir_relpath = "readme",
    #     erase        = True
    # )


# TODO
    # filetest = Path(__file__).parent.parent.parent / "readme" / "about.yaml"

    #

    # for p in xtrct.data.toc:
    #     print(f"+ {p}")
