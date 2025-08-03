#!/usr/bin/env python3

from dataclasses import dataclass


# ------------------------ #
# -- LICENSE DATA CLASS -- #
# ------------------------ #

###
# Easy-to-use data class for licenses.
###
@dataclass(frozen = True)
class License:
    std : str
    name: str
    ref : str

###
# We want to string print the standard code of the license.
###
    def __str__(self) -> str:
        return self.std


###
# prototype::
#     what  : a virtual string path to access the license specified in
#             the analyzed path::‘'about.yaml’' file.
#     where : the folder where to add the file path::''LICENSE.txt''.
#             This folder is indicated using a string path relatively
#             to the folder containing the file path::‘'about.yaml’'.
#     erase : set to ''True'', this \arg allows to erase an existing
#             final file to build a new one.
#
#     :action: creation or update of a path::''LICENSE.txt'' file in
#              the specified folder.
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
