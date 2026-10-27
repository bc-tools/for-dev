### Propose new blocks

Here's how to define a main block.

  1. Add a `YAML` file inside the `contribute/api/block-n-flavour/block/config` folder. The file name corresponds to the block name that will be available to flavours.
  **This name follows the same rules as non-private Python variable names, except that hyphens can replace underscores** (for ease of typing).

  1. Include a mandatory initial magic comment at the beginning of the file to briefly describe the block. **This text will be used for help messages and documentation.** A magic comment starts and ends with `###`.

  1. The structure of the `YAML` file mirrors the structure that users will need to use within the main block.

  1. You can use two types of keys.

      - `key-name` indicates a mandatory key.

      - `key-name *` indicates an optional key.

  1. Rather than providing actual user data values, you must specify the parsers to use. Here is a brief overview. **See the 'Syntax for Block Specifications' section for a complete description and useful guidelines.**

      - For isolated data, simply specify a parser, with the option of using `str` if no parsing is required (meaning `str` keeps the data verbatim as a raw string).

      - For a list of values, use a YAML list with a **single element** of type `parser_name`. **Currently, other dynamic data structures, such as user dictionaries, are not supported.**

  1. You can also add post-processing to a parsed value via a dedicated `Python` function. To do this, simply append a plus sign to the parser name (e.g., `parser_name +`).

  1. Optionally, you can include magic comments to provide additional context or explanations regarding specific blocks.
