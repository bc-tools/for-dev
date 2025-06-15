The `Python` `CLI` and module `multimd`
=======================================

This document is a short tutorial showing all the features.


About `multimd`
---------------

The specific objective of this project is to write `README.md` files for online code repositories. The idea is to write small, separate `MD` files that will then be merged into a single final `MD` file to be seen on the repository.

> *Resources such as images and videos are not managed and never will be. If necessary, use links to resources available on the Internet.*


`README.md` part by part
------------------------

With `multimd`, you can write a `MD` document by typing small section-like parts which are easy to maintain. Consider the `README.md` file from the `multimd` project itself which was written using the following tree on 15 June 2025.

~~~
+ multimd
    * README.md
    + readme
        * about.yaml
        * LICENSE.txt
        * no-about.md
        * prologue.md
        * with-about.md
    + ...
~~~


The special `about.yaml` file is used to specify a specific order in which the different `MD` files are put together (without this file, a "natural" order is used). Its content is as follows: we give the list of the files without their extension.

~~~yaml
toc:
  - prologue
  - about
  - with-about
  - no-about
~~~


> ***CUATION!*** *You can use relative paths but you must use the Unix path separator `/`.*


Building the final `README.md` file is done quickly on the command line after using the `cd` command to go into the `multimd` folder. We use the option `-e` to allow to erase an existing `README.md` file.

~~~bash
> multimd -e readme README.md
Successfully built file.
  + Path given:
    README.md
  + Full path used:
    /full/path/to/README.md
~~~


There is also an easy-to-use `Python` API where `Path` is the class from the `pathlib` module.

~~~python
from multimd import Builder, Path

mybuilder = Builder(
    src   = Path("/full/path/to/readme"),
    dest  = Path("/full/path/to/README.md"),
    erase = True
)
mybuilder.build()
~~~


> ***NOTE.*** *It is possible to work with subfolders containing `MD` files. In this case, `multimd` will work recursively. In the `about.yaml` file, the path to a subfolder simply ends with the Unix path separator `/` like in `one/sub/folder/`.*


Without the special `about.yaml` file
-------------------------------------

Without an `about.yaml` file, all the `MD` files will be merged into one after sorting them in a "natural" order.


> ***WARNING!*** *Without an `about.yaml` file, it is impossible to work with subfolders containing `MD` files. In other words, there will be no recursive search in any subfolders.*
