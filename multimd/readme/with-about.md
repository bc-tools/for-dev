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


> ***CAUTION!*** *You can use relative paths but you must use the Unix path separator `/`.*


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
