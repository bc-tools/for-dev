### Add tools

You may use tools specific to the execution of a code, such as data files added to the final project, as is the case for the data class in `contrib/data/code/licence.py`. Automated code generation tools are also permitted. This type of feature must be coded in the `TOOLS` section comments, which will import the required modules (see the last section, 'Magic Comments', for details).


> ***CAUTION.*** *Do not import modules that are only needed for tools at the beginning of the script, as these imports would otherwise be unnecessarily included in the final product.*


Regarding the addition of supplementary files, you should pay attention to the following points.

  1. Each file must be used in the same folder as the `Python` file. Use relative paths!

  1. The file name must be prefixed by the parser name followed by a hyphen. For example, the data class file `contrib/data/code/license.py` use the additional file `license-spdx.json`.


> ***NOTE.*** *Working with files stored permanently on the end user's operating system is a good practice to adopt for obvious security reasons, as well as for offline use.*
