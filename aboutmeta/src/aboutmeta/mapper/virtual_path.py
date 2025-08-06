
from aboutmeta.data.tocpath   import TOCPath

# --------------- #
# -- CONSTANTS -- #
# --------------- #

TOCPathList = list[TOCPath]



### TODO
# prototype::
#     data : a ''TOCPath'' list.
#
#     :return: the list obtained from data, adding any files from
#              the analysis of path::''about.yaml'' sub-files (cf.
#              the folders indicated in the toc blocks).
###
def map_list(
    amdata_cls: object,
    data_list: TOCPathList
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
