### A new flavour

Here are the steps to follow.

  1. Add a `YAML` file inside the `contrib/api/block-n-flavour/flavour/config` folder. The file name is the flavor name. **This name follows the same rules as non-private Python variable names, except that the hyphen replaces the underscore** (because it's easier to type).

  1. A mandatory initial magic comment at the beginning of the file briefly describes the flavor. **This text will be used for help and documentation.** A magic comment starts and ends with `###`.

  1. The flavor definition is a `YAML` list of unique main block names. There are two kinds of block.

     + `block-name` indicates a mandatory block.

     + `block-name *` indicates an optional block.

  1. If helpful, you can add magic comments to explain the blocks used.
