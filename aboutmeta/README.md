The `Python` module `aboutmeta`
===============================

This document is a complete tutorial showing all the available features.

**Table of contents**

- [What is `aboutmeta`?](#MULTIMD-TOC-ANCHOR-0)
- [`YAML` specifications](#MULTIMD-TOC-ANCHOR-1)
    - [The project itself](#MULTIMD-TOC-ANCHOR-2)
        - [Versionner le projet](#MULTIMD-TOC-ANCHOR-3)
    - [`toc` block](#MULTIMD-TOC-ANCHOR-4)

<a id="MULTIMD-TOC-ANCHOR-0"></a>
What is `aboutmeta`?
--------------------

This project allows metadata to be defined in `about.yaml` files, making it easier for third-party programs to manage digital projects (code projects and document-type projects).

> ***NOTE.*** *A digital project is simply a folder containing content, some of which is only useful during development (tools and tests), while other content is used to create the final product (a computer program or a document to read). In other word, `aboutmeta` is agnostic.*

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

Here are the **conventions used in our explanations**.

1. The concept of attribute will refer to a block, a key, etc.
2. A virtual pointed path like `block-3.key-1` refers to the key `key-1` of block `block-3`.
3. Optional attributes will be indicated by their name followed by an asterisk `*`.
4. Sometimes, an attribute can be used either in the singular or plural form, but not both at the same time. In this case, the name will end with `(s)`, as in `author(s)`.

> ***NOTE.*** *If you are unfamiliar with the general syntax of `YAML`, the [Wikipedia article YAML](https://wikipedia.org/wiki/YAML) is a good place to start.*

---

> ***IMPORTANT.*** *Technically, `YAML` files are read securely by treating all values as simple character strings.*

<a id="MULTIMD-TOC-ANCHOR-2"></a>
### The project itself

Let's start with a complete description of a fictional code project.

~~~yaml
project:
  version*: 0.0.0-beta.1 (2025-06-27)

  acronym* : "[@]bout [Desc]"
  codename*: a_desc
  desc     : Let's explain what is the project ''@Desc''...

  author(s):
    - Ada, Lovelace [ada.babbage.computer@paper.org]
      (Victorian Institute of Applied Mechanical Informatic)
    - Jean, Louis, Krivine [jl-krivine@compile.brain]
    - Torvalds
      (Department of Sacred Kernels, Infernal Ranting Graduate School of Helsinki)

  keywords*:
    - HHH
    - HHH
    - HHH

  licences*:
    code*  : gnu 3
    manual*: cc by 4

  urls*:
    home*  : https://github.com/bc-tools/for-latex
    issues*: https://github.com/bc-tools/for-latex/issues
    dev*   : https://github.com/bc-tools/for-latex/tree/main/tutodoc

  langs*:
    doc*   : fr
    manual*: fr

  require*:
    - python3
    - latex
~~~

In the case of a document-type project, the `project.codename` key is no longer usable and must be replaced by `project.doctitle` (a document must have a title).

> ***NOTE.*** *By default, the project will be considered a code project.*

The following sections detail the use and meaning of the various attributes shown above.

<a id="MULTIMD-TOC-ANCHOR-3"></a>
#### Versionner le projet

La clé optionnel `project.version` sert à identifier la version en cours. Les formats suivants sont pris en compte par `aboutmeta`.

1. `version = 0.0.0-beta.1 (2025-06-27)` ou juste `version = 0.0.0-beta.1`
   [Semantic Versioning](https://semver.org/)
2. `version = 2025-06-27`

<a id="MULTIMD-TOC-ANCHOR-4"></a>
### `toc` block

XXX

~~~yaml
toc:
  - hhh
  - hhh
~~~
