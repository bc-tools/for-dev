#!/usr/bin/env python3


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TOCPathList = list[TOCPath]


# ------------ #
# -- MAPPER -- #
# ------------ #

###
# prototype::
#     amdata_cls : the ''AMData'' class, which will be instantiated
#                  to search recursively for files.
#     data_list  : a ''TOCPath'' list.
#
#     :return: the list obtained from ''data_list'' by adding any
#              files from the analysis of path::''about.yaml'' files
#              (cf. the folders indicated in the ''toc'' blocks).
###
def map_list(
    amdata_cls: object,
    data_list : TOCPathList
) -> TOCPathList:
    final_paths = []

    for data in data_list:
        if data.paths:
            final_paths += data.paths

        else:
            _amdata = amdata_cls(flavour = "toc")
            _amdata.build(yaml_file = data.postsearch)

            final_paths += _amdata.data.toc

    return final_paths
