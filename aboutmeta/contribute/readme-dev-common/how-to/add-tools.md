### Use tools

You may rely on execution utilities and external resources, such as project data files (like the data class in `contribute/api/data/code/licensing.py`). Automated code generation tools are also supported. This functionality must be defined using comments in the 'TOOLS' section, which will import the required modules (see the last section, 'Magic Comments', for details).


> ***CAUTION.*** *Do not place tool-only imports at the beginning of the script. Otherwise, these dependencies will be unnecessarily included in the final `aboutmeta` code.*


Regarding supplementary files, please note the following guidelines.

  1. Each file must be stored in the same directory as the `Python` script. **Always use relative paths!**

  1. File names must be prefixed with the `Python` script name followed by a hyphen. For example, the data class file `contribute/api/data/code/licensing.py` uses the supplementary file `licensing-spdx.json`.


> ***NOTE.*** *Storing files locally on the user's system is recommended for security reasons and ensures offline availability.*
