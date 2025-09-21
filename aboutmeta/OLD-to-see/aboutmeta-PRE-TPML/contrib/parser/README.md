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
- [How to propose new parsing tools?](#MULTIMD-TOC-ANCHOR-4)
    - [How to propose a new parser?](#MULTIMD-TOC-ANCHOR-5)
    - [How to add a post-production tool?](#MULTIMD-TOC-ANCHOR-6)
    - [Tools](#MULTIMD-TOC-ANCHOR-7)
    - [Magic comments](#MULTIMD-TOC-ANCHOR-8)
        - [Complete template](#MULTIMD-TOC-ANCHOR-9)
        - [Imports](#MULTIMD-TOC-ANCHOR-10)
        - [CONSTANTS section (optional)](#MULTIMD-TOC-ANCHOR-11)
        - [PARSER section (mandatory)](#MULTIMD-TOC-ANCHOR-12)
        - [MAPPER section (optional)](#MULTIMD-TOC-ANCHOR-13)
        - [TOOLS section (optional)](#MULTIMD-TOC-ANCHOR-14)
        - [TESTS section (mandatory)](#MULTIMD-TOC-ANCHOR-15)

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

> ***CAUTION.*** *Use a regular `Python` variable name.*

<a id="MULTIMD-TOC-ANCHOR-4"></a>
How to propose new parsing tools? <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
---------------------------------

The following sections outline the steps to follow when proposing new parsing tools.

---

> ***IMPORTANT.*** *A parser works on isolated data, not on lists of data. As these may require complex processing, it will be up to a post-production tools to accomplish this work on lists, not the parser. Keep that in mind.*

---

> ***CAUTION.*** *Regarding `aboutmeta`, you are only authorised to use the modules `aboutmeta.core`, `aboutmeta.tool` and `aboutmeta.specs.data`.* ***Any other use of `aboutmeta` is too risky, as it can create cyclic imports*** *when incorporated validated contributions into the final project.*

---

> ***WARNING.*** *Although it seems more than likely,* ***it is not possible to code a new data class at the same time as new parsing tools.*** *You will therefore have to improvise if you find yourself in this type of situation. That being said, you should always propose your data class first!*

<a id="MULTIMD-TOC-ANCHOR-5"></a>
### How to propose a new parser? <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Here are the steps to follow.

1. Start by finding a name to use when asking to `aboutmeta` to invoke your parser. Don't be lacking in inspiration.
2. The name you choose is the name of the `Python` file where your function for "digesting" isolated data is coded. This function must be named `parse`. Here are **the only possible signatures** for this function.

   - `parse(data)` must be used if only data is to be analyzed, regardless of the location of the `about.yaml` file being analyzed.
   - `parse(parent, data)` also takes into account the folder containing the analyzed `about.yaml` file. The argument `parent` is an instance of `pathlib.Path`.
3. Specific parsing errors must be handled to allow for user input errors for CLI creation of data. This needs the use of `aboutmeta.core.errors.ParsingError` exception class. **It is best to use `from aboutmeta.data.errors import ParsingError`.**
4. You can add other processing functions necessary for the operation of your parser, provided that you do not use the name `map_list`, which is reserved for processing parsed data lists.
5. The “Tools” section explains how to code tools for adding external files, for example.
6. You have to use some magic comments as explained in the last section "Magic comments".

<a id="MULTIMD-TOC-ANCHOR-6"></a>
### How to add a post-production tool? <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Some flavors use data lists that must be modified as a whole once each piece of data has been analyzed by the same parser (for a concrete use case, see the `map_list` function in `contrib/parser/code/virtual_path.py`). This type of functionality is coded in the same file as the common data parser. Here are the steps to follow.

1. By design choice, only "simple" data lists are currently allowed (for example, end users cannot create dictionaries with their own keys). So you just have to code one function `map_list`, which can only have one of the following signatures.

   - `map_list(data_list)` only works with the list of parsed data.
   - `map_list(amdata_cls, data_list)` also takes into account the class `amdata.AMData` to be instanciated.
2. The “Tools” section explains how to code tools for adding external files, for example.
3. You have to use some magic comments as explained in the last section "Magic comments".

<a id="MULTIMD-TOC-ANCHOR-7"></a>
### Tools <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Sometimes, external files are needed, as is the case with the parser `contrib/parser/code/licence.py`. Here's how to work with external files.

1. Each file must be used in the same folder as the `Python` file.
2. The file name must be prefixed by the parser name followed by an hyphen.
3. The files must be added, or build via functions placed in the `TOOLS` section, which will import the necessary modules (see the last section, "Magic Comments", for additional explanations).

---

> ***NOTE.*** *Working with files stored permanently on the end user's operating system is a good practice to adopt for obvious security reasons.*

<a id="MULTIMD-TOC-ANCHOR-8"></a>
### Magic comments <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The `Python` file must comply with the use of certain magic comments. This is necessary for the automation process.

<a id="MULTIMD-TOC-ANCHOR-9"></a>
#### Complete template <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Here is a complete template that will be used to explain how to structure the code in the `Python` file.

~~~python
#!/usr/bin/env python3

...

# ~~ PARSER ~~ #

...

# ~~ MAPPER ~~ #

...

# --------------- #
# -- CONSTANTS -- #
# --------------- #

...

# ~~ PARSER ~~ #

...

# ~~ MAPPER ~~ #

...

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
<a id="MULTIMD-TOC-ANCHOR-10"></a>
#### Imports <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The beginning of the code is where imports are made, with at least the use of `from aboutmeta.data.errors import ParsingError`. You can refine the imports like this.

1. Before the comments `# ~~ PARSER ~~ #` and `# ~~ MAPPER ~~ #`, the imports cover all the coded functions.
2. The comment `# ~~ PARSER ~~ #` is used to indicate imports specific to the `parse` function.
3. The comment `# ~~ MAPPER ~~ #` indicates imports specific to the `map_List` function.

> ***TIP.*** *If you are only coding the parser, the use of the comments `# ~~ PARSER ~~ #` and `# ~~ MAPPER ~~ #` is completely unnecessary.*

<a id="MULTIMD-TOC-ANCHOR-11"></a>
#### CONSTANTS section (optional) <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The rules of use are similar to those that apply to imports, but concern constants.

<a id="MULTIMD-TOC-ANCHOR-12"></a>
#### PARSER section (mandatory) <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This is where the function `parse` is coded, along with any additional utility functions.

<a id="MULTIMD-TOC-ANCHOR-13"></a>
#### MAPPER section (optional) <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This is where the function `map_list` is coded, along with any additional utility functions.

<a id="MULTIMD-TOC-ANCHOR-14"></a>
#### TOOLS section (optional) <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This part of the `Python` file contains tools for development, such as file creation, but not tools needed by the functions `parse` and `map_list`.

> ***WARNING!*** *Remember that each development tool must make its imports internally.*

<a id="MULTIMD-TOC-ANCHOR-15"></a>
#### TESTS section (mandatory) <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

You must produce a minimum number of use cases that will serve as the basis for unit tests for the accepted parsers. **Don't forget to provide functional examples and others with corrupted data!**
