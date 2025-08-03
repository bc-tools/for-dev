#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib     import Path


from aboutmeta.core.DataPrinter import *
from aboutmeta.tool.web        import get_text_from


# --------------- #
# -- CONSTANTS -- #
# --------------- #

URL_TEMPL_SPDX_LICENSE_TEXT = (
    "https://raw.githubusercontent.com/spdx/"
    "license-list-data/main/text/{}.txt"
)


# ------------------------ #
# -- LICENSE DATA CLASS -- #
# ------------------------ #

### TODO
# prototype::
#     std  : str
#     name : str
#     ref  : str
###
@dataclass(frozen = True)
class License(DataPrinter):
    std : str
    name: str
    ref : str

###
# prototype::
#     folder : an existing folder where to add the file path::''LICENSE.txt''.
#     erase  : set to ''True'', this \arg allows to erase an existing
#              final file to build a new one.
#
#     :action: creation or update of a path::''LICENSE.txt'' file in
#              the specified folder.
###
    def add_license(
        self,
        folder: Path,
        erase : bool = False
    ) -> None:
# Does the folder exist?
        if folder.is_dir():
            raise IOError(
                f"the class {type(self).__name__} can't create "
                "the folder:"
                "\n"
                f"{folder}"
            )

# File for the license.
        license_file = folder /  "LICENSE.txt"

# Can we erase an existing final file?
        if license_file.is_file() and not erase:
            raise IOError(
                f"the class {type(self).__name__} is not allowed "
                "to erase the LICENSE file:"
                "\n"
                f"{license_file}"
            )

# Everything looks good. Let's get and the license text.
        license_text = get_text_from(
            URL_TEMPL_SPDX_LICENSE_TEXT.format(self.std)
        )

        license_file.touch()
        license_file.write_text(license_text)


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
    ...
