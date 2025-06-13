`README.md` part by part
------------------------

With `multimd`, you can write a `MD` document by typing small section-like parts which are easy to maintain. Consider the `README.md` file from the `src2prod` project which was written using the following tree on 6 May 2023.

~~~
+ src2prod
    * README.md
    + readme
        * about.yaml
        * about.md
        * build.md
        * cli.md
        * example-used.md
        * only-files.md
        * prologue.md
        * readme-splitted.md
    + ...
~~~


The special `about.yaml` file is used to specify a specific order in which the different `MD` files are put together (without this file, a "natural" order is used). Its content is as follows: we give the list of the files without their extension.

~~~yaml
toc:
  - prologue
  - about
  - example-used
  - build
  - only-files
  - readme-splitted
  - cli
~~~


> ***WARNING!*** *You can use relative paths but you must use the Unix path separator `/`.*


Building the final `README.md` file is done quickly on the command line using `multimd` after using the `cd` command to go into the `src2prod` folder. We use the option `-e` to allow to erase an existing `README.md` file.

~~~bash
> multimd -e readme README.md
Successfully built file.
  + Path given:
    README.md
  + Full path used:
    /full/path/to/README.md
~~~


There is also an easy-to-use `Python` API.

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
