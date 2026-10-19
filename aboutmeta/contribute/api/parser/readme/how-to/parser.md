### From YAML data to internal Python one

Here are the steps to follow.

  1. Start by finding a name to use when asking to `aboutmeta` to invoke your parser. Don't be lacking in inspiration.

  1. The parser name is the `Python` file name where your function for 'digesting' isolated `YAML` data is coded. This function must be named `parse`. Here are **the only possible signatures** for this function (we use generic types for the classes, but you will have to be more precise, as in the accepted parsers).

     + `parse(data: str) -> object` must be used if only data needs to be analyzed, regardless of other of the `about.yaml` file being analyzed.

     + `parse(amdata_cls: object, data: str) -> object` takes into account an instance of the class `aboutmeta.amdata.AMData`. For reference, see the `contrib/parser/code/about_path.py` file.
