The `Python` module `@-bout-meta`
=================================

This document is a complete tutorial showing all the available features.

**Table of contents**

- [What is `@-bout-meta`?](#MULTIMD-TOC-ANCHOR-0)
- [`YAML` specifications](#MULTIMD-TOC-ANCHOR-1)
  - [Block `project`](#MULTIMD-TOC-ANCHOR-2)
  - [Block `toc`](#MULTIMD-TOC-ANCHOR-3)

<a id="MULTIMD-TOC-ANCHOR-0"></a>
What is `@-bout-meta`?
----------------------

This project allows metadata to be defined in `about.yaml` files, making it easier for third-party programs to manage digital projects (code and text).

> ***NOTE.*** *A project refers to a folder containing content, some of which is only useful during development (tools and tests), while other content is used to create the final product (a computer program or a document to be read).*

<a id="MULTIMD-TOC-ANCHOR-1"></a>
`YAML` specifications
---------------------

In this section, we present all level `1` blocks. In the following fictive example, these blocks are named `block-1`, `block-2`, and `block-3`.

~~~yaml
block-1:
  sub-block:
    Some text
    on several lines...

block-2:
  - element 1
  - element 2

block-3:
  - key-1: val-1
  - key-2: val-2
  - key-3s: val-3
~~~
> ***NOTE.*** *If you are unfamiliar with the general syntax of `YAML`, the [Wikipedia article YAML](https://wikipedia.org/wiki/YAML) is a good place to start.*

<a id="MULTIMD-TOC-ANCHOR-2"></a>
### Block `project`

Let's start with a full description of a fictive project.

~~~yaml
project:
  desc   : This class proposes tools for writing "human friendly"
           documentations of LaTeX packages.
  acronym: "[tuto]rial [doc]umentation"
  author : Christophe, BAL

  licences:
    code  : gnu 3
    manual: gnu 3

  urls:
    repo  : https://github.com/bc-tools/for-latex/tree/main/tutodoc
    issues: https://github.com/bc-tools/for-latex/issues

  langs:
    manual: fr

  require:
    - latex
~~~
<a id="MULTIMD-TOC-ANCHOR-3"></a>
### Block `toc`

XXX
