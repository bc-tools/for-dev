How to propose a new parser?
----------------------------

> ***CAUTION!*** *A parser works on isolated data, not lists of data, as these may require complex processing (it will be up to the blocks and flavors to accomplish this work, not the parser.).*

Here are the steps to follow.

  1. Start by finding a name to use when asking to `aboutmeta` to invoke your parser. Don't be lacking in inspiration.

  1. The name you choose is the name of the `Python` file where your function for "digesting" isolated data is coded. This function must be named `parser`. Here are the possible signatures for this function.

     + `parser(data)` XXX

     + `parser(parent, data)` XXX




  and have only one argument `content` corresponding to the text content as typed in the `about.yaml` file.








  1. If necessary, you can add other processing functions needed for your pasrer to work, but be sure to ***read the caution and warning below carefully***.

  1. You are only authorised to use the modules `aboutmeta.data` and `aboutmeta.tool`. ***Any other use of `aboutmeta` is too risky, as it can create cyclic imports when incorporated into the final project.***


---


> ***IMPORTANT!*** *Specific parsing errors must be handled to allow for user input errors for CLI creation of data. This needs the use of `aboutmeta.data.errors.ParsingError` exception class.*


---


> ***CAUTION!*** *If you need external files, as is the case with the parser `contrib/parser/code/licence.py`, you must use them locally and prefix their name by the parser name followed by an hyphen. These files must be added, or build via functions placed in the `TOOLS` section, which will import the necessary modules.* **This choice allows to provide only files that are permanently stored on the end user's operating system.** *This is a best practice imposed for obvious security reasons.*


---


> ***WARNING!*** *You must follow the template below and use the long and tedious access to constants, functions, and classes of the `Python` `aboutmeta` module. This is necessary for the automation process. But, if you do not need any imports, tools or constants, you can skip the associated sections.* ***In manual tests, don't forget to provide functional examples and corrupted data that can be added to the unit tests!***

~~~python
#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

from aboutmeta.data.errors import ParsingError

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
