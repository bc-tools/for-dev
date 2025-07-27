#!/usr/bin/env python3

from aboutmeta.data.pre_amdata import *


# -------------------------- #
# -- ABOUTMETA DATA CLASS -- #
# -------------------------- #

###
# The “AMData” class implements the methods needed to actually extract
# and validate the data.
###
class AMData(PreAMData):
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

###
# prototype::
#     data : the ''tocpath.TOCPath'' list returned by the parser is
#            used for a recursive analysis of subfolders, if necessary.
#
#     :return: the list of files found.
###
    def post_toc(
        self,
        data : List[TOCPath],
    ) -> List[Path]:
        final_paths = []
        xtrct       = AMData()

        for onedata in data:
            if onedata.kind == TAG_TOC_PATH_FILES:
                final_paths += onedata.paths

            else:
                xtrct.build(
                    yaml_file = onedata.paths,
                    keep      = SET_KEEP_ONLY_TOC
                )

                final_paths += xtrct.data.toc

        return final_paths
