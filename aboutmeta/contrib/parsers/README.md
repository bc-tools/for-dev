Add new plugins to `aboutmeta`
==============================

Structure of the `contrib/parsers` folder
-----------------------------------------

### The `STATUS` subfolder

This folder allows you to know the status of your proposal.


### Other subfolders

The folders correspond to the main blocks of the `about.yaml` file. In their subfolders, you will find at least one `Python` file named `default.py`, which corresponds to the default behavior of the `Python` `aboutmeta` module.


How to propose new parsers?
---------------------------

The easiest way is to copy and paste the `default.py` file, then adapt it to your proposal without changing the signature of the `dataparser` function. It is preferable to propose a name that corresponds to the parameter used by the user of aboutmeta, but if you don't have any ideas, use your name to name your `Python` file.


> ***CAUTION!*** *If you need external files, as is the case with the parser `contrib/parsers/licences/default.py`, you must provide a function prefixed with `tool_` that is responsible for creating this file.* **This choice allows to provide only files that are stored permanently on the end user's operating system.** *This is a best practice imposed for obvious security reasons.*


> ***WARNING!*** *You must keep the following template and use the long and tedious access to constants, functions, and classes of the `Python` `aboutmeta` module. This is necessary for the automation process.*

~~~python
#!/usr/bin/env python3

import aboutmeta


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

...


# ----------------------------- #
# -- HUMAN TESTS (MANDATORY) -- #
# ----------------------------- #

if __name__ == "__main__":
    ...
~~~
