### Post-production tools

Some flavors use `YAML` data lists that must be modified as a whole once each piece of data has been analyzed by the same parser (for a concrete use case, see the `map_list` function in `contrib/parser/code/virtual_path.py`).


By design choice, only 'simple' data lists are currently allowed (for example, end users cannot create dictionaries with their own keys). So you just have to code one function `map_list`, which can only have one of the following signatures (here, we use generic types for the classes, but you will have to be more precise, as in the accepted parsers).

   + `map_list(data_list: object) -> object` only works with a list of parsed data.

   + `map_list(amdata_cls: object, data_list: object) -> object` takes into account an instance of the class `aboutmeta.amdata.AMData`.
