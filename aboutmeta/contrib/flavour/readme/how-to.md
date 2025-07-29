How to propose a new flavour?
-----------------------------

A flavor is defined using aromas which are for us the main building blocks. You can therefore contribute by adding new blocks and/or new flavours.


### A new block

Here's how to define a main block.

  1. The name of the `YAML` file is the name of the block that will be usable by flavors.

  1. The `YAML` structure reflects the one that the user will have to use.

  1. Instead of user data, you must specify the parsers to be used. Let's quickly explain what can be done (see the section *“Syntax for block specifications”* for a complete description).

     + For isolated data, simply specify a parser, with the additional option of using `str` if no parser is to be used (the data must be kept in string form).

     + For a list of values, use a `YAML` list with a single element of type `list(parser_name)`.

  1. For lists of values, it may be useful to add post-processing of the entire list of individually parsed values. In this case, simply use `list(parser_name) +` with an additional final plus sign.

  1. Finally, you must provide short messages describing data to be entered via magic comments. These texts will be used when creating data via the CLI (see the section *“Syntax for block specifications”* to see how to do this).


### A new flavour

Here's how to define a main block.

  1. The name of the `YAML` file is the name of the flavour that will be usable by the user.

  1. The `YAML` structure

????


For now, it is only possible to provide a `YAML` list of blocks without repetition. The file must starts with a small description that willl be printed if dat are created with the CLI.

~~~yaml
####
# This flavor is used to define an IT project, a code or a document,
# with the option to work with a list of specific files via a "table
# of contents".
###

- project*
- toc*
~~~
