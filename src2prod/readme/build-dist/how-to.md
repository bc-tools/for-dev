### How to do that?

The parameters are specified in the `about.yaml` file where the `dist` key is the one that talks to `src2prod` (the `YAML` file can use other main keys). For our fictitious project, we use the `ignore` subkey to indicate which files and folders to ignore that are still kept by `git` (a rule ending by `/` is for folders). We also specify the `README.md` file to put in the output code.

''`yaml
dist:
  # We use a relative path.
  readme: README.md
  # We work with multiline content, this is why
  # we use the pipe character.
  ignore: |
    tool_*/
    tool_*.*
''`

> ***NOTE:*** *it is possible to use finer settings. See the documentation for more information.*

Here is how to make a selective copy from the sub-directory `src` to the sub-folder `mockproject`. We will assume that the `cd` command has been used beforehand, so that running the `Python` scripts is done from the development folder `MockProject`.

~~~python
from src2prod import Project, Path

project = Project(
    project = Path('MockProject'),
    erase   = True
)

project.build()
~~~


The same effect can be done directly with the following command (using `cd` and a relative path works also).

~~~
> scr2prod -e /full/path/to/MockProject
~~~


In both cases, we have to allow `src2prod` to erase the product folder to build it: see the `Python` argument `erase`, and the command line flag `-e`.


>
> ***NOTE:*** *errors and warnings will be printed in the terminal, and also written verbatim to the file `mockproject.src2prod.log`.*
