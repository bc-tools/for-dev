The `Python` module `src2prod`
==============================


> **I beg your pardon for my english...**
>
> English is not my native language, so be nice if you notice misunderstandings, misspellings, or grammatical errors in my documents and codes.


About `src2prod`
----------------

This module allows to develop a project within a source folder and to publish the final product in another folder, this last directory being a "thin" version of the source one. If you use `git`, this module can talk with it to do a better job. 


### One example - A `Python` project

#### What we have...

Let's consider [`TeXitEasy`](https://github.com/projetmbc/tools-for-latex/tree/master/TeXitEasy)  which had merly the following tree structure on August 9, 2021 (this was the very begining of this project).

~~~
+ TeXitEasy
    + changes
        + 2021
            * 08.txt
        * LICENSE.txt
        * x-todo-x.txt

    + src
        * __init__.py
        * escape.py
        * LICENSE.txt
        + tool_config
            * escape.peuf
        * tool_debug.py
        * tool_escape.py

    + tests
        + escape
            * escape.peuf
            * fstringit.peuf
            * test_fstringit.py
            * test_escape.py
    * about.peuf
    * pyproject.toml
    * README.md
~~~


#### What we want...

In the tree above, there are some files just useful for the development of the code.

  1. Names using the pattern `x-...-x` indicate files or folders to be ignored by `git` (there are no such file or folder in the `src` folder but we could imagine using some of them).

  1. Names using the pattern `tool_...` are for files and folders to not copy into the final product, but at the same time to be kept by `git`.

  1. The `README.md` file used for `git` servers must also be used for the final product.


The final product built from the `src` folder must have the following name and structure. 

~~~
+ texiteasy
    * __init__.py
    * escape.py
    * LICENSE.txt
    * README.md
~~~


#### How to do that?

Here is how to acheive a selective copy of the `src` folder to the `texiteasy` one. We will suppose the use of the `cd` command to go inside the parent folder of `TeXitEasy` before launching the following script where we use instances of `Path` from `pathlib`.

~~~python
from src2prod import *

project = Project(
    project = Path('TeXitEasy'),
    source  = Path('src'),
    target  = Path('texiteasy'),
    ignore  = '''
        tool_*/
        tool_*.*
    ''',
    usegit = True,
    readme = Path('README.md')
)

project.update()
~~~

Here are some important points about the code above.

  1. `project`, `source`, `target` and `readme` follows the rules below.

        * The values of this arguments can also be strings (that will be converted to instances of `Path`).
        
        * The argument `readme` is optional contrary to `project`, `source` and `target`.

        * `project` is a complete path regarding the working directory when launching the file, but `source`, `target` and `readme` are relative to `project`.

  1. The rules for the argument `ignore` follow the `gitignore` syntax. You can use this argument even if you don't work with `git`.

  1. `usegit = True` asks to ignore files and folders as `git` does. This also implies that there isn't any uncommited files in the `src` folder.

  1. Errors and warnings are printed in the terminal and written verbosely in the file `TeXitEasy.src2prod.log` where `TeXitEasy` is the name extracted from the path `project`.


### All the source files to copy

Sometimes the final product is not just a "selective clone" of the `src` folder: for example, it can be a melting of several source files in a single final one (the author of `src2prod` uses this technic to develop his `LaTeX` projects). In such a case, you can use the following method and attribut.

  1. The method `build` just looks for the files to keep for the `texiteasy` folder.

  1. The attribut `lof` is the list of all files to keep in the `src` folder (`lof` is for `list of files`).

Here is an example of code printing the list of only the source files to keep.

~~~python
from src2prod import *

project = Project(
    name   = 'TeXitEasy',
    source = Path('src'),
    target = Path('texiteasy'),
    ignore = '''
        tool_*/
        tool_*.*
    ''',
    usegit = True,
    readme = Path('README.md')
)

project.build()

for f in project.lof:
    print(f)
~~~

This script gives the following output in a terminal. Note that the list doesn't contain the path of the `README` file, this last one must be manage by hand (see the methods `check_readme` and `copy_readme` of the class `Project`). 

~~~
/full/path/to/TeXitEasy/src/__init__.py
/full/path/to/TeXitEasy/src/escape.py
/full/path/to/TeXitEasy/src/LICENSE.txt
~~~


<!-- :tutorial-START: -->
<!-- :tutorial-END: -->


<!-- :version-START: -->
<!-- :version-END: -->