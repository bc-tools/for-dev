The `Python` module `@-bout-meta`
=================================

This document is a complete tutorial showing all the available features.

**Table of contents**

- [What is `about-meta`?](#MULTIMD-TOC-ANCHOR-0)
- [`YAML` specifications](#MULTIMD-TOC-ANCHOR-1)
    - [Block `project`](#MULTIMD-TOC-ANCHOR-2)
        - [`version`](#MULTIMD-TOC-ANCHOR-3)
    - [Block `toc`](#MULTIMD-TOC-ANCHOR-4)

<a id="MULTIMD-TOC-ANCHOR-0"></a>
What is `about-meta`?
---------------------

This project allows metadata to be defined in `about.yaml` files, making it easier for third-party programs to manage digital projects (code and text).

> ***NOTE.*** *A digital project is simply a folder containing content, some of which is only useful during development (tools and tests), while other content is used to create the final product (a computer program or a document to read). In other word, `about-meta` is agnostic.*

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
  - key-3: val-3
~~~
> ***NOTE.*** *If you are unfamiliar with the general syntax of `YAML`, the [Wikipedia article YAML](https://wikipedia.org/wiki/YAML) is a good place to start.*

<a id="MULTIMD-TOC-ANCHOR-2"></a>
### Block `project`

Let's start with a complete description of a fictional project (detailed explanations are provided immediately afterwards, although the example should be self-explanatory).

~~~yaml
project:
  version: 0.0.0-beta.1
  dates  :
    - start
    - last

  acronym: "[@]bout [Desc]"
  usename: a_desc

  desc   : Let's explain what is the project ''@Desc''...
  authors:
    - Ada, Lovelace [ada.babbage.computer@paper.org]
      (Victorian Institute of Applied Mechanical Informatic)
    - Jean, Louis, Krivine [jl-krivine@compile.brain]
    - Torvalds
      (Department of Sacred Kernels, Infernal Ranting Graduate School of Helsinki)

  keywords:
    - HHH

  licences:
    code  : gnu 3
    manual: cc by 4

  urls:
    home  : https://github.com/bc-tools/for-latex/issues
    issues: https://github.com/bc-tools/for-latex/issues
    dev   : https://github.com/bc-tools/for-latex/tree/main/tutodoc

  langs:
    doc   : fr
    manual: fr

  require:
    - python3
    - latex
~~~
<a id="MULTIMD-TOC-ANCHOR-3"></a>
#### `version`

XXX

<a id="MULTIMD-TOC-ANCHOR-4"></a>
### Block `toc`

XXX

~~~yaml
toc:
  - hhh
  - hhh
~~~
