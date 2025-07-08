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

The easiest way is to copy and paste the `default.py` file, then adapt it to your proposal without changing the signature of the `dataparser` function. Use your name to name your `Python` file.

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
