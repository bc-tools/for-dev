Add new plugins to `aboutmeta`
==============================

Structure of the `contrib/parser` folder
----------------------------------------

### The `STATUS` subfolder

This folder allows you to know the status of your proposal. Its structure mimics the `contrib/parser` one.


### Other subfolders

The folders correspond to the data structure of the `about.yaml` file. In the deepest subfolders, you will find at least one `Python` file named `default.py` corresponding to the default behavior.


> ***NOTE.*** *If you want to create a parser that does not exist by default, simply follow the structure of the `about.yaml` file in the folder structure of `contrib/parser`.*


How to propose a new parser?
----------------------------

Here are the steps to follow.

  1. Start by finding a name to use when calling `aboutmeta` to invoke your parser. *If you're stuck for inspiration, use your surname.*

  1. The name you choose is the name of the `Python` file where you will implement your data digestion function, which must be named `parser` and have only one argument `content` corresponding to the text content as typed in the `about.yaml` file.

  1. If necessary, you can add other processing functions, but be sure to read the caution and warning below carefully.


---


> ***CAUTION!*** *If you need external files, as is the case with the parser `contrib/parsers/licences/default.py`, you must use them locally. These files must be added, or build via functions placed in the `TOOLS` section, which will import the necessary modules.* **This choice allows to provide only files that are permanently stored on the end user's operating system.** *This is a best practice imposed for obvious security reasons.*


---


> ***WARNING!*** *You must follow the template below and use the long and tedious access to constants, functions, and classes of the `Python` `aboutmeta` module. This is necessary for the automation process. But, if you do not need any imports, tools or constants, you can skip the associated sections.* ***In manual tests, don't forget to provide functional examples and corrupted data that will be added to the unit tests!***

~~~python
#!/usr/bin/env python3

import aboutmeta


# ------------- #
# -- IMPORTS -- #
# ------------- #

...


# --------------- #
# -- CONSTANTS -- #
# --------------- #

...


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

...


# ----------- #
# -- TOOLS -- #
# ----------- #

...


# ----------------- #
# -- HUMAN TESTS -- #
# ----------------- #

if __name__ == "__main__":
    ...
~~~
