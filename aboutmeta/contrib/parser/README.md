Add new plugins to `aboutmeta`
==============================

Structure of the `contrib/parser` folder
----------------------------------------

### The `STATUS` subfolder

This folder allows you to know the status of your proposal. Its structure mimics the `contrib/parser` one.


### Other subfolders

The folders correspond to the main blocks of the `about.yaml` file. In their subfolders, you will find at least one `Python` file named `default.py`, which corresponds to the default behavior of the `Python` `aboutmeta` module.


How to propose new parsers?
---------------------------

The easiest way is to copy and paste the `default.py` file, then adapt it to your proposal without changing the signature of the `dataparser` function. It is preferable to propose a name that corresponds to the parameter used by the user of aboutmeta, but if you don't have any ideas, use your name to name your `Python` file.


> ***NOTE.*** *In manual tests, don't forget to provide functional examples and corrupted data that will be added to the unit tests!*


---


> ***CAUTION!*** *If you need external files, as is the case with the parser `contrib/parsers/licences/default.py`, you must use them locally. These files must be added, or build via functions placed in the `TOOLS` section, which will import the necessary modules.* **This choice allows to provide only files that are permanently stored on the end user's operating system.** *This is a best practice imposed for obvious security reasons.*


---


> ***WARNING!*** *You must follow the template below and use the long and tedious access to constants, functions, and classes of the `Python` `aboutmeta` module. This is necessary for the automation process. But, if you do not need any imports, tools or constants, you can skip the associated sections.*

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
