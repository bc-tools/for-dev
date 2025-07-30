<!----------------------------------------------------------------
  -- File created by the ''multimd'' project, version 1.0.0.    --
  --                                                            --
  -- ''multimd'', soon to be available on PyPI, is developed at --
  -- https://github.com/bc-tools/for-dev/tree/main/multimd      --
  ---------------------------------------------------------------->


Add new parsers to aboutmeta
============================

**Table of contents**

<a id="MULTIMD-GO-BACK-TO-TOC"></a>
- [Structure of the "contrib/parser" folder](#MULTIMD-TOC-ANCHOR-0)
    - [The changes folder](#MULTIMD-TOC-ANCHOR-1)
    - [The status folder](#MULTIMD-TOC-ANCHOR-2)
    - [The code folder](#MULTIMD-TOC-ANCHOR-3)
- [How to propose a new parser?](#MULTIMD-TOC-ANCHOR-4)
- [How to add a post-production tool?](#MULTIMD-TOC-ANCHOR-5)

<a id="MULTIMD-TOC-ANCHOR-0"></a>
Structure of the "contrib/parser" folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
----------------------------------------

<a id="MULTIMD-TOC-ANCHOR-1"></a>
### The changes folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This folder is just a communication tool between contributors to indicate important changes.

<a id="MULTIMD-TOC-ANCHOR-2"></a>
### The status folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This folder allows you to know the status of your proposal. Its structure mimics the folder of contributions: `YAML` files correspond to contribution files.

<a id="MULTIMD-TOC-ANCHOR-3"></a>
### The code folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This folder contains all the parsers. A file named `myparser.py` will correspond to `myparser` in a `YAML` specification file.

<a id="MULTIMD-TOC-ANCHOR-4"></a>
How to propose a new parser? <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
----------------------------

> ***CAUTION!*** *A parser works on isolated data, not on lists of data. As these may require complex processing, it will be up to a post-production tool to accomplish this work, not the parser. The next section explains how to add post-production tools.*

---

Here are the steps to follow.

1. Start by finding a name to use when asking to `aboutmeta` to invoke your parser. Don't be lacking in inspiration.
2. The name you choose is the name of the `Python` file where your function for "digesting" isolated data is coded. This function must be named `parser`. Here are **the only possible signatures** for this function.

   - `parse(data)` must be used if only data is to be analyzed, regardless of the location of the `about.yaml` file being analyzed.
   - `parse(parent, data)` also takes into account the folder containing the analyzed `about.yaml` file. The argument `parent` is an instance of `pathlib.Path`.
3. If necessary, you can add other processing functions needed for your parser to work, but be sure to **read the caution and warning below carefully**.
4. You are only authorised to use the modules `aboutmeta.data` and `aboutmeta.tool`. **Any other use of `aboutmeta` is too risky, as it can create cyclic imports when incorporated validated contributions into the final project.**

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
<a id="MULTIMD-TOC-ANCHOR-5"></a>
How to add a post-production tool? <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
----------------------------------

Some flavors use lists of data of the same type that require modification as a whole once each piece of data has been parsed: for a real-world use case, see the description of the `map_list` function inside `contrib/parser/code/virtual_path.py`.

The coding is done in the same folder as the isolated data parser via the `map_list` function, which can only have one of the following signatures.

- `map_list(data_list)` only works with the list of parsed data.
- `map_list(parent, data_list)` also takes into account the folder containing the analyzed `about.yaml` file. The argument `parent` is an instance of `pathlib.Path`.

---

> ***CAUTION!*** By design choice, only "simple" data lists are currently allowed (for example, end users cannot create dictionaries with their own keys).
