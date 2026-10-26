### Post-production tools

Sometimes data require some actions to be performed: for instance: for instance, the `about_path` parser needs to build a full list of absolute paths based on raw paths and/or search patterns (see `contrib/parser/code/about_path.py`).

By design, only one post-processing step can be defined, through the function `postprod`, using only one of the following signatures (here, we use generic types for the classes, but you will have to be more precise, as in the accepted parsers).

   + `postprod(data: object) -> object` only works with the data.

   + `postprod(amdata: object, data: object) -> object` also takes into account an instance of the class `aboutmeta.amdata.AMData`.


> ***CAUTION.*** *Never use `from aboutmeta.amdata import AMData`, type `amdata` as `object`, and use `new_amdata = amdata.new_instance(flavour=..., file=...)` for new `AMData` instances.*


The `postprod` function can process two kinds of `data`.

   + For a single parser in the YAML specifications, `data` is just the data built by the `parse` function.

   + For a list of data parsed in the YAML specifications, `data` is a list of data built by the `parse` function.
