<!----------------------------------------------------------------
  -- File created by the ''multimd'' project, version 1.0.0.    --
  --                                                            --
  -- ''multimd'', soon to be available on PyPI, is developed at --
  -- https://github.com/bc-tools/for-dev/tree/main/multimd      --
  ---------------------------------------------------------------->


Add new flavours to aboutmeta
=============================

**Table of contents**

<a id="MULTIMD-GO-BACK-TO-TOC"></a>
- [Structure of the "contrib/block-n-flavour" folder](#MULTIMD-TOC-ANCHOR-0)
    - [The changes folder](#MULTIMD-TOC-ANCHOR-1)
    - [The status folder](#MULTIMD-TOC-ANCHOR-2)
    - [The block folder](#MULTIMD-TOC-ANCHOR-3)
    - [The flavour folder](#MULTIMD-TOC-ANCHOR-4)
- [How to propose a new flavour?](#MULTIMD-TOC-ANCHOR-5)
    - [A new flavour](#MULTIMD-TOC-ANCHOR-6)
    - [A new block](#MULTIMD-TOC-ANCHOR-7)
- [Syntax for block specifications](#MULTIMD-TOC-ANCHOR-8)
    - [Structure](#MULTIMD-TOC-ANCHOR-9)
    - [Special keys](#MULTIMD-TOC-ANCHOR-10)
    - [Shortcut for the last parser used](#MULTIMD-TOC-ANCHOR-11)
    - [Magic comments](#MULTIMD-TOC-ANCHOR-12)
        - [General block description](#MULTIMD-TOC-ANCHOR-13)
        - [How certain blocks and keys work](#MULTIMD-TOC-ANCHOR-14)
        - [The special case of alternatives](#MULTIMD-TOC-ANCHOR-15)

<a id="MULTIMD-TOC-ANCHOR-0"></a>
Structure of the "contrib/block-n-flavour" folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
-------------------------------------------------

<a id="MULTIMD-TOC-ANCHOR-1"></a>
### The changes folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This folder is just a communication tool between contributors to indicate important changes.

<a id="MULTIMD-TOC-ANCHOR-2"></a>
### The status folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This folder allows you to know the status of your proposal. Its structure mimics the folder of contributions: `YAML` files correspond to contribution files.

<a id="MULTIMD-TOC-ANCHOR-3"></a>
### The block folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This folder contains `YAML` files specifying main blocks, which serve as building blocks for creating flavours.

<a id="MULTIMD-TOC-ANCHOR-4"></a>
### The flavour folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This folder contains `YAML` configuration files defining flavours.

<a id="MULTIMD-TOC-ANCHOR-5"></a>
How to propose a new flavour? <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
-----------------------------

A flavor is defined using aromas which are for us the main blocks. You can therefore contribute by adding new blocks and/or new flavours.

<a id="MULTIMD-TOC-ANCHOR-6"></a>
### A new flavour <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Here are the steps to follow.

1. Add a `YAML` file inside the `contrib/block-n-flavour/flavour` folder. The file name is the flavor name. **This name follows the same rules as non-private Python variable names, except that the hyphen replaces the underscore** (because it's easier to type).
2. A magic comment at the beginning of the file briefly describes the flavor. **This text will be used by the CLI as help.**
3. The flavor definition is an unordered `YAML` list of unique main block names. Don't forget that blocks are dictionary keys. There are two kinds of block.

   - `block-name` indicates a mandatory block.
   - `block-name *` indicates an optional block.

Here is the code used for the `it-project` flavour.

~~~yaml
###
# This flavor allows to define an IT project (code or document),
# with the option of working with a list of specific files via
# a "table of contents".
###

- project*
- toc*
~~~
<a id="MULTIMD-TOC-ANCHOR-7"></a>
### A new block <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Here's how to define a main block.

1. Add a `YAML` file inside the `contrib/flavour/block` folder. The name of the `YAML` file is the name of the block that will be usable by flavors. **This name follows the same rules as non-private Python variable names, except that the hyphen replaces the underscore** (because it's easier to type).
2. A magic comment at the beginning of the file briefly describes the flavor. **This text will be used by the CLI as help.**
3. The structure of the `YAML` file reflects the structure that the user will need to use in the main block.
4. You can use two types of key.

   - `key-name` indicates a mandatory key.
   - `key-name*` indicates an optional key.
5. Instead of values corresponding to future user data, you need to specify the parsers to be used. Let's quickly explain what can be done. **See section *"Syntax for block specifications"* for a complete description with some useful guidelines.**

   - For isolated data, simply specify a parser, with the additional option of using `str` if no parser is to be used (in other words, `str` is for data to keep verbatim in string form).
   - For a list of values, use a `YAML` list with a **single element** of type `parser_name`. **At present, no other "dynamic" data, like user dictionnaries, can't be used.**
6. **For lists of values**, it may be useful to add post-processing of the entire list of individually parsed values. In this case, simply use `parser_name+` with an additional final plus sign.
7. Finally, magic comments must describe shortly the block and its data. These texts will be used by the CLI as help. **See the section *"Syntax for block specifications"* to see how to do this.**

<a id="MULTIMD-TOC-ANCHOR-8"></a>
Syntax for block specifications <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
-------------------------------

<a id="MULTIMD-TOC-ANCHOR-9"></a>
### Structure <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The structure of the specifications mimics those that the user will be able to use, with the exception of lists, which require the use of a single element list. In concrete terms, here's how it looks with a simplified extract from of the `project` block (in its August 7, 2025 version).

~~~yaml
# Simplified extract from ''project.yaml'' file,
# version of August 7, 2025.

version: sem_version
desc: str
urls:
  home  : url
  dev   : url
  issues: url
require:
  - str
~~~

This code allows to use data such as the following, where the version will be analyzed by the `sem_version` parser, and URLs by the `url` parser. The `desc` data and the ones of the `require` list are kept as string values.

~~~yaml
# Fake example.

version: 1.0.0
desc: Just a basic fake example.
urls:
  home  : https://xkcd.com/2973
  dev   : https://xkcd.com/1923
  issues: https://xkcd.com/1686
require:
  - python
  - yaml
~~~
<a id="MULTIMD-TOC-ANCHOR-10"></a>
### Special keys <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

A little DSL allows you to define some special features for keys. Here's what you can use.

1. To indicate **an optional key**, simply add the `*` character after its name, as in `key-name*`.
2. An **alternative choice of keys**, i.e. only one key from a set of keys is allowed, use the character `|` as in `key-1-not-2 | key-2-not-1`, and if the keys are optional, simply use `key-1-not-2 | key-2-not-1 *`. You can use as many characters `|` as you need. Then, for the associated value, you have to use a similiar list of parsers like in `key-1-not-2 | key-2-not-1 : parser_1 | parser_2`.

> ***NOTE.*** *If one of the key is a list of data, just use `list(parser_name)`.*

Here is almost real extract extract from of the `project` block (in its August 7, 2025 version).

~~~yaml
# Almost real uncommented extract from ''project.yaml'' file,
# version of August 7, 2025.

version*: sem_version
date*: date

acronym*: str
desc: str

author | authors *: person | list(person)

urls*:
  home*  : url
  dev*   : url
  issues*: url

require*:
  - str
~~~
<a id="MULTIMD-TOC-ANCHOR-11"></a>
### Shortcut for the last parser used <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

There's a shortcut to avoid typing the same parser name several times in succession: just use a period. Bear in mind that in the actual extract below, the use of `person | list(.)` marks the `person` parser, which is reused in `list(.)`, but that the default parser does not become `list(person)`, which is not a parser, therefor `author` and `contrib` use the same parser.

~~~yaml
# Uncommented real extract from ''project.yaml'' file,
# version of August 7, 2025.

version*: sem_version
date*: date

acronym*: str
desc: .

author | authors *: person | list(.)
contrib | contribs *: . | list(.)

urls*:
  home*  : url
  dev*   : .
  issues*: .

require*:
  - str
~~~
<a id="MULTIMD-TOC-ANCHOR-12"></a>
### Magic comments <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

A new block definition must contain a minimum of documentation (these texts will be used as help by the CLI). Here are the situations to be taken into account (using the `project.yaml` file as an example, version August 7, 2025).

<a id="MULTIMD-TOC-ANCHOR-13"></a>
#### General block description <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The following code shows how to succinctly describe the purpose of the block via a comment at the very beginning of the `YAML` specification file.

~~~yaml
###
# This block allows to describe a project from a technical point
# of view.
###

...
~~~
<a id="MULTIMD-TOC-ANCHOR-14"></a>
#### How certain blocks and keys work <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

After the general description, it is possible - and strongly recommended - to document blocks or keys, but nothing is imposed. Documentation is added in the comments just before the block or key concerned. Here are a few extracts from the `project.yaml` file, where, in the case of the `urls` block, it should be noted that there is no need to document the `home`, `dev` and `issues` keys.

~~~yaml
...

###
# This is the current version number of the project.
###
version*: sem_version

...

###
# Three kinds of URL can be given.
#
#   + ''home'' is for the website of the project, the human one.
#
#   + ''dev'' is dedicated to the repository of the project, this
#     is not intended for human beings.
#
#   + ''issues'' allows regular users to report bugs.
###
urls*:
  home*  : url
  dev*   : .
  issues*: .

...
~~~
<a id="MULTIMD-TOC-ANCHOR-15"></a>
#### The special case of alternatives <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Documentation of an alternative requires that the various competing keys be documented in sections indicated by magic titles of the form `{key-name}`, as in the following example.

~~~yaml
...

###
# {codename}
# This value, optional for a code-type project, allows to name the
# project differently from the folder containing it.
#
# {doctitle}
# This value is mandatory for a “document” type project: it gives
# the title of the document.
###
codename | doctitle *: . | .

...
~~~
