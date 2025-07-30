How to add a post-production tool?
----------------------------------

Some flavors use data lists that must be modified as a whole once each piece of data has been analyzed by the same parser (for a concrete use case, see the `map_list` function in `contrib/parser/code/virtual_path.py`). This type of functionality is coded in the same file as the common data parser via the `map_list` function, which can only have one of the following signatures.

  + `map_list(data_list)` only works with the list of parsed data.

  + `map_list(parent, data_list)` also takes into account the folder containing the analyzed `about.yaml` file. The argument `parent` is an instance of `pathlib.Path`.


---


> ***CAUTION!*** By design choice, only "simple" data lists are currently allowed (for example, end users cannot create dictionaries with their own keys).
