<!-- This file was generated using the Python package `multimd`. -->

The `Python` `CLI` and module `multimd`
=======================================

This document is a complete tutorial showing all the available features.

**Table of contents**

<a id="MULTIMD-GO-BACK-TO-TOC"></a>
- [What is `multimd`?](#MULTIMD-TOC-ANCHOR-0)
- [`README.md` part by part](#MULTIMD-TOC-ANCHOR-1)
- [Without the special `about.yaml` file](#MULTIMD-TOC-ANCHOR-2)
- [Finishing touches](#MULTIMD-TOC-ANCHOR-3)
    - [What is done automatically?](#MULTIMD-TOC-ANCHOR-4)
    - [ToC settings](#MULTIMD-TOC-ANCHOR-5)

<a id="MULTIMD-TOC-ANCHOR-0"></a>
What is `multimd`? <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
------------------

The specific objective of this project is to write single `README.md` file for online code repositories. The idea is to write small, separate `MD` files that will then be merged by `multimd` into a single final `MD` file to be seen on the repository.

> ***CAUTION!*** *The main process is based on the [markdown-it-py](https://github.com/executablebooks/markdown-it-py) and [markdownify](https://github.com/matthewwithanm/python-markdownify/tree/master) projects, so the limitations of `multimd` therefore come from these projects, but the unit tests show a fairly robust behaviour.*

<a id="MULTIMD-TOC-ANCHOR-1"></a>
`README.md` part by part <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
------------------------

With `multimd`, you can write a `MD` document by typing small section-like files which are easy to maintain. Consider the `README.md` file from the `multimd` project itself which was written using the following tree on 23 June 2025 (the day of the version `1.0.0`).

~~~
+ multimd
    * README.md
    + readme
        * about.yaml
        * LICENSE.txt
        * no-about.md
        * prologue.md
        * standard.md
        * with-about.md
    + ...
~~~

The special `about.yaml` file is used to specify a specific order in which the different `MD` files are put together (without this file, a "natural" order is used). Its content is as follows: we give the list of the files without their extension.

~~~yaml
toc:
  - prologue
  - about
  - with-about
  - no-about
  - standard
~~~
> ***NOTE.*** *It is possible to specify relative paths, but this requires the use of the Unix path separator `/`.*

Building the final `README.md` file is done quickly on the command line after using the `cd` command to go into the `multimd` folder. We use the option `-e` to allow to erase an existing `README.md` file.

~~~bash
> multimd -e readme README.md
Successfully built file.
  + Path given:
    README.md
  + Full path used:
    /full/path/to/README.md
~~~

There is also an easy-to-use `Python` API where `Path` is the class from the `pathlib` module.

~~~python
from multimd import Builder, Path

mybuilder = Builder(
    src   = Path("/full/path/to/readme"),
    dest  = Path("/full/path/to/README.md"),
    erase = True
)
mybuilder.build()
~~~
> ***NOTE.*** *It is possible to work with subfolders containing `MD` files. In this case, `multimd` will work recursively. In the `about.yaml` file, the path to a subfolder simply ends with the Unix path separator `/` like in `one/sub/folder/`.*

<a id="MULTIMD-TOC-ANCHOR-2"></a>
Without the special `about.yaml` file <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
-------------------------------------

Without an `about.yaml` file, all the `MD` files found will be merged into one after sorting them in a "natural" order.

> ***WARNING!*** *Without an `about.yaml` file, it is impossible to work with subfolders containing `MD` files. In other words, there will be no recursive search in any subfolders.*

<a id="MULTIMD-TOC-ANCHOR-3"></a>
Finishing touches <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
-----------------

<a id="MULTIMD-TOC-ANCHOR-4"></a>
### What is done automatically? <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

During final formatting, `multimd` standardises the source code to prevent `git` from spotting any *'false-positive'* changes. Here's what happens behind the scenes.

1. **Add a table of contents**, with hyperlinks, via the alias `::TOC::` that can be used **only alone on one line and only once**. See the following section for more details.
2. **Section titles** use the non-standard, but very visual, syntax of `===` and `---` for the first two levels of section, and then consecutive `#` symbols are used.
3. **Removal of unnecessary spaces**.
4. **Management of consecutive blank lines**: excluding formatted code, consecutive blank lines are reduced to a single one.
5. **Add a blank line** after an `MD` block, if necessary.

<a id="MULTIMD-TOC-ANCHOR-5"></a>
### ToC settings <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

In the following code, the alias `::TOC::` will be replaced by a full table of contents, with hyperlinks, in the final document. In fact, the first level `1` heading is never added, as it is the title of the document.

~~~md
...
My project
==========

Let's put *the table of contents here*.

::TOC::

Let's continue writing **our content**.
...
~~~

By default, all sections from level `2` onwards are included in the table of contents (level `1` corresponds to the document title). You can specify the maximum depth `<depth>` of the table of content sections to be retained using `::TOC-<depth>::`.

- `::TOC-1::` requests that only sections of level `2` are retained.
- `::TOC-2::` requests that only sections of level `2` or `3` are retained.
- And so on...
