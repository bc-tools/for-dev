### Magic comments

The `Python` file must comply with the use of certain magic comments. Here is a complete template that will explain how to structure the code in the `Python` file.


~~~python
#!/usr/bin/env python3

# ------------- #
# -- IMPORTS -- #
# ------------- #

... [IMP-1]

# ~~ PARSER ~~ #

... [IMP-2]

# ~~ MAPPER ~~ #

... [IMP-3]

# --------------- #
# -- CONSTANTS -- #
# --------------- #

... [CST-1]

# ~~ PARSER ~~ #

... [CST-2]

# ~~ MAPPER ~~ #

... [CST-3]

# ------------ #
# -- PARSER -- #
# ------------ #

...

# ------------ #
# -- MAPPER -- #
# ------------ #

...

# ----------- #
# -- TOOLS -- #
# ----------- #

...

# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    ...
~~~


Let's explain how to use the code sections "IMPORTS", "CONSTANTS", "PARSER", "MAPPER", "TOOLS" and "TESTS".

  1. `IMPORTS` section: XXX

  1. `CONSTANTS` section: XXX

  1. `PARSER` section: XXX

  1. `MAPPER` section: XXX

  1. `TOOLS` section: XXX

  1. `TESTS` section: XXX



> ***WARNING!*** *You must follow the template below. This is necessary for the automation process. But, if you do not need any imports, tools, constants or humant tests, you can skip the associated sections.* ***In manual tests, don't forget to provide functional examples and corrupted data that can be added to the unit tests!***
