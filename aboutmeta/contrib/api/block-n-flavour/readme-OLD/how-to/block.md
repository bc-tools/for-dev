### A new block

Here's how to define a main block.

  1. Add a `YAML` file inside the `contrib/api/block-n-flavour/block/config` folder. The name of the `YAML` file is the name of the block that will be usable by flavors. **This name follows the same rules as non-private Python variable names, except that the hyphen replaces the underscore** (because it's easier to type).






  1. ????
  A magic comment at the beginning of the file describes peecisely the block. **This text will be used by the CLI as help, and automataicllay used for .**











  1. The structure of the `YAML` file reflects the structure that the user will need to use in the main block.

  1. You can use two types of key.

      + `key-name` indicates a mandatory key.

      + `key-name *` indicates an optional key.

  1. Instead of values corresponding to future user data, you need to specify the parsers to be used. Let's quickly explain what can be done. **See section *"Syntax for block specifications"* for a complete description with some useful guidelines.**

     + For isolated data, simply specify a parser, with the additional option of using `str` if no parser is to be used (in other words, `str` is for data to keep verbatim in string form).

     + For a list of values, use a `YAML` list with a **single element** of type `parser_name`. **At present, no other "dynamic" data, like user dictionnaries, can't be used.**

  1. **For lists of values**, it may be useful to add post-processing of the entire list of individually parsed values. In this case, simply use `parser_name+` with an additional final plus sign.

  1. Finally, magic comments must describe shortly the block and its data. These texts will be used by the CLI as help. **See the section *"Syntax for block specifications"* to see how to do this.**
