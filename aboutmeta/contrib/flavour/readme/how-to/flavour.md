### A new flavour

Here are the steps to follow.

  1. Add a `YAML` file inside the `contrib/flavour/config` folder. The file name is the flavor name. **This name follows the same rules as non-private Python variable names, except that the hyphen replaces the underscore** (because it's easier to type).

  1. The flavor definition is an unordered `YAML` list of unique main block names. Don't forget that blocks are dictionary keys. There are two kinds of block.

     + `block-name` indicates a mandatory block.

     + `block-name *` indicates an optional block.

  1. A magic comment at the beginning of the file briefly describes the flavor. This text will be used by the CLI as help.


Here is the code used for the `it-project` flavour.

~~~yaml
###
# This flavor is used to define an IT project, a code or a document,
# with the option to work with a list of specific files via a "table
# of contents".
###

- project *
- toc *
~~~
