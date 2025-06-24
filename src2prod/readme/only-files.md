Only the source files to copy
-----------------------------

Sometimes, the final product is not just a "selective clone" of the folder `src`: for example, a final file may be the merging of several source files (the author of `src2prod` uses this technique to develop his `LaTeX` projects). In such a case, you can use the following method and attribute.

  1. The method `check` just looks for files to keep for the product folder without creating anything.

  1. After the use of `check`, the attribute `lof` is the list of all files to be kept from the `src` folder (`lof` means *"list of files "* and not *"laugh out frankly"*).

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


> ***Note:*** *the list does not contain the path to a `README.md` file or a `readme` folder: if needed, see the `check_readme` and `copy_readme` methods of the class `Project`.*
