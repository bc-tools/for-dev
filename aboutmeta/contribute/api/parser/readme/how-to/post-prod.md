### Post-production tools






XXXXX



Some flavors use `YAML` data lists that must be modified as a whole once each piece of data has been analyzed by the same parser (for a concrete use case, see the `post_prod` function in `contrib/parser/code/about_path.py`).


By design choice, only 'simple' data lists are currently allowed (for example, end users cannot create dictionaries with their own keys). So you just have to code one function `post_prod`, which can only have one of the following signatures (here, we use generic types for the classes, but you will have to be more precise, as in the accepted parsers).

   + `post_prod(data: object) -> object` only works with a list of parsed data.

   + `post_prod(amdata: object, data: object) -> object` takes into account an instance of the class `aboutmeta.amdata.AMData`.
