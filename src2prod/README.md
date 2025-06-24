The `Python` module `src2prod`
==============================

> **I beg your pardon for my english...**
>
> English is not my native language, so be nice if you notice misunderstandings, misspellings, or grammatical errors in my documents and codes.

This document is a very short tutorial presenting some features without being exhaustive.


About `src2prod`
----------------

This module allows to develop a project within a source folder and to publish the final code product in another folder, this last directory being a "thin" version of the source one. If you use `git`, this module can talk with it to do a better job.


The example used for this short tutorial
----------------------------------------

We will consider a fictitious development project `MockProject` with the following tree structure where the `about.yaml` file is important to talk to `src2prod`.

~~~
+ MockProject
    * about.yaml
    * pyproject.toml
    * README.md
    + changes
        + 2022
            * 12.txt
        * LICENSE.txt
        * x-todo-x.txt
    + src
        * __init__.py
        * LICENSE.txt
        * mockthis.py
        * x-roadmap-x.txt
        + tool_config
            * settings.yaml
        * tool_debug.py
        * tool_mockthis.py
    + tests
        + mockthis
            * bad_input.yaml
            * test_bad_input.py
~~~


Building a thin copy of the source folder
-----------------------------------------


### What we want...

In the project `MockProject`, there are some files that are only useful for code development.

  1. Names using the pattern `x-...-x` indicate files or folders that `git` must ignore: see `x-roadmap-x.txt` in the `src` directory.

  1. Names using the pattern `tool_...` are for files and folders not to be included in the final product, but which `git` must retain.

  1. The `README.md` file used for `git` servers must also be included in the final product code.


By copying files, we wish to add one new folder `mockproject`, in lower case, to obtain the following structure.

~~~
+ MockProject
    * about.yaml
    * pyproject.toml
    * README.md
    + changes [...]
    + mockproject
        * __init__.py
        * mockthis.py
        * LICENSE.txt
        * README.md
    + src [...]
    + tests [...]
~~~


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

> ***NOTE:*** *it is possible to make finer settings. See the documentation for more information.*

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


Only the source files to copy
-----------------------------

Sometimes, the final product is not just a "selective clone" of the folder `src`: for example, a final file may be the merging of several source files (the author of `src2prod` uses this technique to develop his `LaTeX` projects). In such a case, you can use the following method and attribute.

  1. The method `check` just looks for files to keep for the product folder without creating anything.

  1. After the use of `check`, the attribute `lof` is the list of all files to be kept from the `src` folder (`lof` is for *"list of files"*).

Here is an example of code that prints the list of source files to be kept for the final product.

~~~python
from src2prod import Project, Path

project = Project(
    project = Path('MockProject'),
    readme  = Path('README.md')
)

project.check()

for f in project.lof:
    print(f)
~~~

This script run in a terminal gives the following output.

~~~
/full/path/to/MockProject/src/__init__.py
/full/path/to/MockProject/src/mockthis.py
/full/path/to/MockProject/src/LICENSE.txt
~~~


> ***Note:*** *the list does not contain the path to a `README` file or a `readme` folder: if needed, see the `check_readme` and `copy_readme` methods of the class `Project`.*


`README.md` piece-by-piece
--------------------------

You can write your `README.md` by typing `MD` chunks. Let's assume we have done this for our fictitious development project `MockProject` which now has the following tree structure.

~~~
+ MockProject
    * about.yaml
    * pyproject.toml
    + changes [...]
    + readme
        * about.md
        * about.yaml
        * cli.md
        * escape.md
        * prologue.md
    + src [...]
    + tests [...]
~~~


The special file `readme/about.yaml` is used here to specify the order in which the different `MD` files are merged. Its contents is as follows where the `toc` key is for *"table of contents"*.

~~~yaml
toc:
  - prologue
  - about
  - mockthis
  - cli
~~~

The construction of the new final product `mockproject` is very simple: we just specify the folder `readme` instead of a file in the `MockProject/about.yaml` file which is now the following one.

''`yaml
dist:
  # We use a relative path with the character /
  # at the end to say that we give a folder.
  readme: readme/
  ignore: |
    tool_*/
    tool_*.*
''`


That's all folks!
