### Propose new flavours

Here are the steps to follow.

  1. Add a YAML file inside the `contribute/api/block-n-flavour/flavour/config` folder. The file name must match the flavour name.
  **This name follows the same rules as non-private Python variable names, except that hyphens can replace underscores** (for ease of typing).

  1. Include a mandatory magic comment at the beginning of the file to briefly describe the flavour. **This text will be used for help and documentation.** A magic comment starts and ends with `###`.

  1. The flavour definition is a `YAML` list of unique main block names. There are two kinds of blocks.

      - `block-name` indicates a mandatory block.

      - `block-name *` indicates an optional block.


> ***NOTE.*** *Each block comes with its own mandatory documentation, eliminating the need to document individual blocks within a flavor definition.*
