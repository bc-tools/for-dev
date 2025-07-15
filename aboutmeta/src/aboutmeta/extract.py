#!/usr/bin/env python3

from pathlib import Path
from yaml    import safe_load

from aboutmeta.data.boxplus import BoxPlus

from aboutmeta.parser import (
    date,
    lang,
    license,
    person,
    version,
)

from aboutmeta.specs import *
from aboutmeta.style import ALL_STYLES


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAG_STYLE_DEFAULT = 'default'


# -------------------------------------------------- #
# -- XXXX -- #
# -------------------------------------------------- #

class Extract:
    def __init__(
        self,
        style = TAG_STYLE_DEFAULT
    ):
        self.style = style

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


    def build(
        self,
        yaml_file
    ):
        self._yaml_file_dir = yaml_file.parent

        self.data = BoxPlus(
            self.__recu_parse(
                safe_load(yaml_file.read_text()),
                SPECS_PARSING
            )
        )

    def __recu_parse(
        self,
        data,
        specs
    ):
        data_parsed = {}

# Illegal alternatives?
        if specs[TAG_SPECS_ALT_ALL]:
            keys_set   = set(data.keys())
            to_analyze = keys_set.intersection(
                set(specs[TAG_SPECS_ALT_ALL])
            )

            print(f"{to_analyze=}")

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
                        x
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


    def validate_urls(self):
        ...

    def add_license(self):
        ...


if __name__ == "__main__":
    filetest = Path(__file__).parent.parent.parent / "about.yaml"
    filetest = Path(__file__).parent.parent.parent / "readme" / "about.yaml"

    xtrct = Extract()
    xtrct.build(filetest)

    from pprint import pprint
    pprint(xtrct.data.project.toc)
