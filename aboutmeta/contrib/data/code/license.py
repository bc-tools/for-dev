#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib     import Path

from aboutmeta.core.dataprinter import DataPrinter
from aboutmeta.tool.web         import get_text_from


# --------------- #
# -- CONSTANTS -- #
# --------------- #

_URL_TEMPL_SPDX_LICENSE_TEXT = (
    "https://raw.githubusercontent.com/spdx/"
    "license-list-data/main/text/{}.txt"
)


# ------------------------ #
# -- LICENSE DATA CLASS -- #
# ------------------------ #

###
# prototype::
#     std  : the short SPDX identifier, such as ''GPL-3.0-only''.
#     name : the full license name like ''GNU General Public
#            License v3.0 only''.
#     ref  : the URL linking to the SPDX online description of
#            the license.
#
#
# note::
#     The ''std'' attribute is part of the frozen dataclass
#     ''DataPrinter''.
###
@dataclass(frozen = True)
class License(DataPrinter):
    name: str
    ref : str

###
# prototype::
#     folder : the path to an existing folder in which to add
#              the path::''LICENSE.txt'' file.
#     erase  : if this option is set to ''True'', it allows to
#              delete an existing final file in order to create
#              a new one.
#
#     :action: create or update a path::''LICENSE.txt'' file in
#              the specified folder with the complete text of
#              the license.
###
    def add_license(
        self,
        folder: Path,
        erase : bool = False
    ) -> None:
# Does the folder exist?
        if not folder.is_dir():
            raise IOError(
                f"the class {type(self).__name__} can't create "
                f"the folder:\n{folder}"
            )

# File for the license.
        license_file = folder /  "LICENSE.txt"

# Can we erase an existing final file?
        if license_file.is_file() and not erase:
            raise IOError(
                f"the class {type(self).__name__} is not allowed "
                f"to erase the LICENSE file:\n{license_file}"
            )

# Everything seems to be in order. Let's proceed with the
# recovery, then add the license text.
        license_text = get_text_from(
            _URL_TEMPL_SPDX_LICENSE_TEXT.format(self.std)
        )

        license_file.touch()
        license_file.write_text(license_text)


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
    lic = License(
        std  = "GPL-3.0-only",
        name = "",
        ref  = ""
    )

    this_dir = Path(__file__).parent
    lic_file = this_dir / "LICENSE.txt"

    lic.add_license(
        folder = this_dir,
        erase  = True
    )

    first_2_lines = lic_file.read_text().splitlines()[:2]

    assert first_2_lines == [
        'GNU GENERAL PUBLIC LICENSE',
        'Version 3, 29 June 2007'
    ]

    lic_file.unlink()
