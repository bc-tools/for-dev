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
- [Structure of the "contrib/flavour" folder](#MULTIMD-TOC-ANCHOR-0)
    - [The changes folder](#MULTIMD-TOC-ANCHOR-1)
    - [The status folder](#MULTIMD-TOC-ANCHOR-2)
    - [The block folder](#MULTIMD-TOC-ANCHOR-3)
    - [The config folder](#MULTIMD-TOC-ANCHOR-4)
- [How to propose a new flavour?](#MULTIMD-TOC-ANCHOR-5)
    - [A new block](#MULTIMD-TOC-ANCHOR-6)
    - [A new flavour](#MULTIMD-TOC-ANCHOR-7)
- [Syntax for block specifications](#MULTIMD-TOC-ANCHOR-8)
    - [Comments for helping messages](#MULTIMD-TOC-ANCHOR-9)
    - [YAML structure](#MULTIMD-TOC-ANCHOR-10)

<a id="MULTIMD-TOC-ANCHOR-0"></a>
Structure of the "contrib/flavour" folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
-----------------------------------------

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
### The config folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This folder contains `YAML` configuration files defining flavours.

<a id="MULTIMD-TOC-ANCHOR-5"></a>
How to propose a new flavour? <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
-----------------------------

A flavor is defined using aromas which are for us the main building blocks. You can therefore contribute by adding new blocks and/or new flavours.

<a id="MULTIMD-TOC-ANCHOR-6"></a>
### A new block <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Here's how to define a main block.

1. The name of the `YAML` file is the name of the block that will be usable by flavors.
2. The `YAML` structure reflects the one that the user will have to use.
3. Instead of user data, you must specify the parsers to be used. Let's quickly explain what can be done (see the section *“Syntax for block specifications”* for a complete description).

   - For isolated data, simply specify a parser, with the additional option of using `str` if no parser is to be used (the data must be kept in string form).
   - For a list of values, use a `YAML` list with a single element of type `list(parser_name)`.
4. For lists of values, it may be useful to add post-processing of the entire list of individually parsed values. In this case, simply use `list(parser_name) +` with an additional final plus sign.
5. Finally, you must provide short messages describing data to be entered via magic comments. These texts will be used when creating data via the CLI (see the section *“Syntax for block specifications”* to see how to do this).

<a id="MULTIMD-TOC-ANCHOR-7"></a>
### A new flavour <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Here's how to define a main block.

1. The name of the `YAML` file is the name of the flavour that will be usable by the user.
2. The `YAML` structure

????

For now, it is only possible to provide a `YAML` list of blocks without repetition. The file must starts with a small description that willl be printed if dat are created with the CLI.

~~~yaml
####
# This flavor is used to define an IT project, a code or a document,
# with the option to work with a list of specific files via a "table
# of contents".
###

- project*
- toc*
~~~
<a id="MULTIMD-TOC-ANCHOR-8"></a>
Syntax for block specifications <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
-------------------------------

<a id="MULTIMD-TOC-ANCHOR-9"></a>
### Comments for helping messages <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

POur comprendre ce qu'il faut faire, nous allons exraire une partie du fichier `flavor/block/project.yaml`.

~~~yaml
###
# This block allows to describe a project from a technical point of
# view.
###


###
# This is the current version number of the project.
###
version*: version
###
# This is the date of the current version of the project.
###
date*: date
###
# This information explains the meaning of the acronym used to name
# the project.
###
acronym*: str
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
###
# You need to describe shortly your project.
###
desc: .
###
# {author}
# For a single author, you have the following possible syntaxes.
#
#   + ''Krivine'' , ''Louis, Krivine'' and ''Jean, Louis, Krivine''
#     are legal titles for a person (the number of first names is
#     unlimited).
#
#   + ''Krivine [jlk@brain.fr]'' adds an email.
#
#   + ''Krivine (L'Institut du Cerveau, France)'' adds an institute.
#
#   + ''Krivine [jlk@brain.fr] (L'Institut du Cerveau, France)''
#     mixes the previous features.
#
# {authors}
# For severals authors, just use a YAML list of single authors (see
# the description of the key ''author'').
###
author | authors *: person | list(.)

###
# {contrib}
# For a single contributor, the syntaxes allowed are similar to the
# ones for a single author (see the key ''author'').
#
# {contribs}
# For severals authors, just use a YAML list of single authors (see
# the description of the key ''author'').
###
contrib | contribs *: . | list(.)

###
# Three kinds of URL can be given.
#
#   + ''home'' is for the website of the project, the human one.
#
#   + ''dev'' is dedicated to the repository of the project, this is
#     not intended for human beings.
#
#   + ''issues'' allows regular users to report bugs.
###
urls*:
  home*  : url
  dev*   : .
  issues*: .
###
# Granting a license is a good practice.
#
#   + ''code'' is for the code of the project.
#
#   + ''manual'' is for the manual of the project.
###
licenses*:
  code*  : license
  manual*: .
###
# This for the language used to write the manual (manual) and the
# technical (doc) documentations.
###
langs*:
  doc*   : lang
  manual*: .

###
# Don't forget to give the list of the required general tools needed
# to make your project functional.
###
require*: list(str)

###
# Providing a list of keywords describing the project helps to better
# understand its usefulness.
###
keywords*: list(.)
~~~
<a id="MULTIMD-TOC-ANCHOR-10"></a>
### YAML structure <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

XXXX

~~~yaml
###
# This block allows to describe a project from a technical point of
# view.
###


###
# This is the current version number of the project.
###
version*: version
###
# This is the date of the current version of the project.
###
date*: date
###
# This information explains the meaning of the acronym used to name
# the project.
###
acronym*: str
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
###
# You need to describe shortly your project.
###
desc: .
###
# {author}
# For a single author, you have the following possible syntaxes.
#
#   + ''Krivine'' , ''Louis, Krivine'' and ''Jean, Louis, Krivine''
#     are legal titles for a person (the number of first names is
#     unlimited).
#
#   + ''Krivine [jlk@brain.fr]'' adds an email.
#
#   + ''Krivine (L'Institut du Cerveau, France)'' adds an institute.
#
#   + ''Krivine [jlk@brain.fr] (L'Institut du Cerveau, France)''
#     mixes the previous features.
#
# {authors}
# For severals authors, just use a YAML list of single authors (see
# the description of the key ''author'').
###
author | authors *: person | list(.)

###
# {contrib}
# For a single contributor, the syntaxes allowed are similar to the
# ones for a single author (see the key ''author'').
#
# {contribs}
# For severals authors, just use a YAML list of single authors (see
# the description of the key ''author'').
###
contrib | contribs *: . | list(.)

###
# Three kinds of URL can be given.
#
#   + ''home'' is for the website of the project, the human one.
#
#   + ''dev'' is dedicated to the repository of the project, this is
#     not intended for human beings.
#
#   + ''issues'' allows regular users to report bugs.
###
urls*:
  home*  : url
  dev*   : .
  issues*: .
###
# Granting a license is a good practice.
#
#   + ''code'' is for the code of the project.
#
#   + ''manual'' is for the manual of the project.
###
licenses*:
  code*  : license
  manual*: .
###
# This for the language used to write the manual (manual) and the
# technical (doc) documentations.
###
langs*:
  doc*   : lang
  manual*: .

###
# Don't forget to give the list of the required general tools needed
# to make your project functional.
###
require*: list(str)

###
# Providing a list of keywords describing the project helps to better
# understand its usefulness.
###
keywords*: list(.)
~~~
