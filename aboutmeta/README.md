The `Python` module `aboutmeta`
===============================

This document is a complete tutorial showing all the available features.

**Table of contents**

- [What is `aboutmeta`?](#MULTIMD-TOC-ANCHOR-0)
- [`YAML` specifications](#MULTIMD-TOC-ANCHOR-1)
    - [The project itself](#MULTIMD-TOC-ANCHOR-2)
            - [Version and date](#MULTIMD-TOC-ANCHOR-3)
        - [Project identity.](#MULTIMD-TOC-ANCHOR-4)
        - [Developers, authors and contributors](#MULTIMD-TOC-ANCHOR-5)
        - [URLs of the project](#MULTIMD-TOC-ANCHOR-6)
        - [Licences](#MULTIMD-TOC-ANCHOR-7)
        - [Languages](#MULTIMD-TOC-ANCHOR-8)
        - [Technologies required](#MULTIMD-TOC-ANCHOR-9)
        - [Keywords](#MULTIMD-TOC-ANCHOR-10)
    - [Working with folders and files](#MULTIMD-TOC-ANCHOR-11)
- [The `Python` module `aboutmeta`](#MULTIMD-TOC-ANCHOR-12)
    - [Data extraction](#MULTIMD-TOC-ANCHOR-13)
    - [Use of data](#MULTIMD-TOC-ANCHOR-14)
        - [The project itself](#MULTIMD-TOC-ANCHOR-15)
            - [Version and date](#MULTIMD-TOC-ANCHOR-16)
            - [Developers, authors and contributors](#MULTIMD-TOC-ANCHOR-17)
            - [URLs of the project](#MULTIMD-TOC-ANCHOR-18)
            - [Licences](#MULTIMD-TOC-ANCHOR-19)
            - [Languages](#MULTIMD-TOC-ANCHOR-20)
        - [Working with folders and files](#MULTIMD-TOC-ANCHOR-21)

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
project*:
  version*: 0.0.0-beta.1 (2025-06-27)

  acronym* : "[@]bout [Desc]ription"
  codename*: a_desc
  desc     : Let's explain what is the project ''@Desc''...

  author(s):
    - Ada, Lovelace  [ada.babbage.computer@paper.org]
      (Victorian Institute of Applied Mechanical Informatic)
    - Jean, Louis, Krivine  [jl-krivine@compile.brain]
    - Torvalds
      (Department of Sacred Kernels, Infernal Ranting Graduate School of Helsinki)
    - William, Justme

  contrib(s)*:
    - Alan, Turing  [alan.turing@enigma.uk]
      (Institut de Cryptographie Avancée)
    - Donald, Knuth  [donald.knuth@texmath.net]
      (Université de la Typographie du TeX-as)

  urls*:
    home*  : https://github.com/bc-tools/for-dev
    dev*   : https://github.com/bc-tools/for-dev/tree/main/aboutmeta
    issues*: https://github.com/bc-tools/for-dev/issues

  licences*:
    code*  : gpl 3.0+
    manual*: cc by nc 4.0

  langs*:
    doc*   : f
    manual*: fr

  require*:
    - python3
    - latex

  keywords*:
    - metadata
    - coding
    - writing
~~~
> ***NOTE.*** *In the case of a document-type project, the `project.codename` key is no longer usable and must be replaced by `project.doctitle` (a document must have a title). By default, the project will be considered a code project.*

The following sections detail the use and meaning of the various attributes shown above.

<a id="MULTIMD-TOC-ANCHOR-3"></a>
##### Version and date

The optional `project.version` key is used to identify the current version, with the following formats being natively supported by the `Python` module `aboutmeta`.

1. `2025-06-27` indicates a date in the English format `YYYY-MM-DD`.
2. `0.0.0-beta.1` indicates a version number respecting ["Semantic Versioning"](https://semver.org/).
3. `0.0.0-beta.1 (2025-06-27)` is a combination of version and date.

<a id="MULTIMD-TOC-ANCHOR-4"></a>
#### Project identity.

The keys `project.acronym`, `project.codename`, `project.doctitle`, and `project.desc` are used to quickly identify a project.

> ***IMPORTANT.*** *Note that the `desc` key is mandatory. Furthermore, `codename` and `doctitle` can never be used at the same time.*

Here is how these different keys are used.

1. `desc` is used to quickly describe the project.
2. `acronym` explains the origin of an acronym: for example, `"[@]bout [Desc]ription"` explains the choice for the project name `@Desc`.
3. `codename` allows you to specify the name of a code-type project if it differs from that of the project folder (this convention is widely used).
4. `doctitle` must be used for a document-type project. This is because such a project must have a title.

> ***NOTE.*** *The last two points show that `aboutmeta` will assume that it is working with a code-type project by default.*

<a id="MULTIMD-TOC-ANCHOR-5"></a>
#### Developers, authors and contributors

The keys `project.author`, which is mandatory, and `project.contrib`, which is optional, are used either in the singular to indicate a single person, or in the plural to indicate a list of people. Here is a fictitious use case.

~~~yaml
project:
  author: Ada, Lovelace

  contribs:
    - Alan, Turing
    - Donald, Knuth
~~~

The following forms of personal identification are managed by the `Python` module `aboutmeta`.

1. **Title (mandatory):** `Surname`, `First name, Compound surname`, `First name 1, First name 2, Long surname`... Hereinafter, we will refer to one of the above forms as `<title>`.
2. **Email address (optional):** `<title> [un.id@provider.abc]` uses square brackets for the email.
3. **Affiliation (optional):** `<title> (Name of institute)` uses parentheses for the affiliation.
4. **Indicate everything:** only the format `<title> [email] (institute)` is allowed.

> ***NOTE.*** *Emails are not verified.*

<a id="MULTIMD-TOC-ANCHOR-6"></a>
#### URLs of the project

The optional `project.url` block allows you to provide hyperlinks via the following keys, all of which are optional.

1. `home` allows you to specify the address of a website dedicated to the project.
2. `dev` is used to point to a repository for managing project development.
3. `issues` redirects users to the page where they can report bugs or make suggestions.

> ***NOTE.*** *It is possible to request verification of the validity of URLs by the `Python` module `aboutmeta`. Technically, a simple DNS query is performed, and nothing more is done for security reasons.*

<a id="MULTIMD-TOC-ANCHOR-7"></a>
#### Licences

The optional block `project.licences` is used to indicate licences via the following keys (no formats supported at this time).

1. `code` is for the licence of the code or document relating to the project.
2. `manual` allows, in the case of a code-type porject, the selection of a licence specific to the user manual.

The `Python` module `aboutmeta` takes into account the licence names proposed by the [`SPDX` SPDX License List](https://spdx.org/licenses/).

> ***NOTE.*** *You can request the addition of a `LICENCE.txt` file in the folder containing the `about.yaml` file.*

<a id="MULTIMD-TOC-ANCHOR-8"></a>
#### Languages

The optional `project.langs` block allows you to specify the languages used for the following cases related to a code-type project.

1. The `doc` key is for the language used to write the technical documentation.
2. The `manual` key is for the language used to write the user manual.

Language names must be those recognised by the `Python` package [`Babel`](https://babel.pocoo.org/en/latest/) used behind the scenes: see [ISO 639 standard](https://en.wikipedia.org/wiki/ISO_639) for languages and [ISO 3166 standard](https://en.wikipedia.org/wiki/ISO_3166) for countries. For example, `fr_FR` indicates French spoken in France.

> ***NOTE.*** *The default language is `en_GB`.*

<a id="MULTIMD-TOC-ANCHOR-9"></a>
#### Technologies required

Using the optional `project.require` block, it is possible to provide a list of programming languages required for the code to work, or for compiling a document, this depends on the type of project.
For the record, we reproduce the fictitious example presented at the beginning of this document.

~~~yaml
project:
  require:
    - python3
    - latex
~~~
<a id="MULTIMD-TOC-ANCHOR-10"></a>
#### Keywords

Keywords are used to categorise the type of project succinctly: this is done via the optional `project.keywords` key. Here is the example we proposed at the beginning of the document.

~~~yaml
project:
  keywords:
    - metadata
    - coding
    - writing
~~~
<a id="MULTIMD-TOC-ANCHOR-11"></a>
### Working with folders and files

Whether for a document written in small sections or for a monorepo project, it is useful to be able to specify a **list of existing folders and/or files** to explore in a customised order.
The optional `toc` block meets this need. Its content must be a list of relative paths, with folders indicated by a slash ‘/’ at the end of the path, which also serves as a path separator, even when working with the Windows operating system.
Here is a fictitious example.

~~~yaml
toc:
  - relative/path/to/file_1.txt
  - relative/path/to/one/folder/
  - relative/path/inside/one/sub/folder/file_2.md
~~~

When a folder is specified, this means that it contains an `about.yaml` file that must also be analysed.

> ***NOTE.*** *Using the `Python` module `aboutmeta`, it is possible to specify a default extension.*

<a id="MULTIMD-TOC-ANCHOR-12"></a>
The `Python` module `aboutmeta`
-------------------------------

In addition to providing `YAML` specifications, that can be used in your preferred programming language, `aboutmeta` offers a `Python` module based on a plugin system that handles certain data formats.
The following sections describe what is available in the current version.

> ***NOTE.*** *The `contrib/parsers` folder contains a `README.md` file explaining how to easily build and suggest new parsers.*

<a id="MULTIMD-TOC-ANCHOR-13"></a>
### Data extraction

The analysis of an `about.yaml` file is done simply as follows where `Path` is the class from the `pathlib` module.

~~~python
from aboutmeta import Extract, Path

meta = Extract(Path("/full/path/to/about.yaml"))
meta.build()
~~~
<a id="MULTIMD-TOC-ANCHOR-14"></a>
### Use of data

Once the data has been extracted by `aboutmeta.AboutMeta`, the `data` attribute of the `meta` object, see the previous section, provides access to the digested data in a simple manner.

1. If we take the example given in the specifications, access to the home URL is done via `meta.data.project.urls.home`, which is ideal for non-dynamic code.
2. For dynamic coding, it is possible to use a virtual pointed path as in `meta["project.urls.home"]`.

The following sections present the data after digestion. **To keep things simple, we will always use access to data processed via the `data` attribute, and work with the `meta` object explained in the previous section.**

> ***NOTE.*** *To retrieve the original `YAML` version of a piece of data, there is the `verbatim` attribute, as in `meta.verbatim.project.version`, which is a standardised version of the original text.*

<a id="MULTIMD-TOC-ANCHOR-15"></a>
#### The project itself

We only present digested data that does not reproduce the contents of the `YAML` file.

<a id="MULTIMD-TOC-ANCHOR-16"></a>
##### Version and date

Let's assume that the `YAML` file contains the data `version: 1.2.3-beta.4+build.5 (2025-06-27)`. By default, the digest will provide the following information.

1. The version number is accessible via the `meta.data.project.version.nb` attribute, whose text version is simply `1.2.3-beta.4+build.5`.
   For a detailed analysis, you can use the following sub-attributes.

   - `major` provides the integer `1`.
   - `minor` provides the integer `2`.
   - `patch` provides the integer `3`.
   - `prerelease` provides the text `beta.4`.
   - `v.build` provides the text `build.5`.
2. The version date is accessible via the attribute `meta.data.project.version.date`, whose text version is simply `2025-06-27`.
   If needed, you can use the following sub-attributes.

   - `year` provides the integer `2025`.
   - `month` provides the integer `6`.
   - `day` provides the integer `27`.

> ***NOTE*** *Behind the scenes, the version number is a `semver.version.Version` object, while the date is a `datetime.date` object (which provides access to all the methods associated with these types of objects).*

<a id="MULTIMD-TOC-ANCHOR-17"></a>
##### Developers, authors and contributors

> ***NOTE.*** *For the `project.author(s)` and `project.contrib(s)` keys, the digested data is always a list of identifiers. In other words, the singular forms `project.author` and `project.contrib` will produce a list of size 1. This choice allows for unified management of the digested data.*

The elements of the list are `aboutmeta.person.Person` objects that have the following sub-attributes.

1. `firstnames` is the list of first names.
2. `surname` is the surname.
3. `email` is to the text written in parentheses.
4. `affiliation` is to the text written in square brackets.

<a id="MULTIMD-TOC-ANCHOR-18"></a>
##### URLs of the project

Although URLs are stored verbatim, we would like to point out here that `aboutmeta.Extract` is capable of testing the validity of URLs in the sense that they are associated with a DNS catalogue. In other words, a URL that points nowhere will cause an error.
As this operation involves a basic, risk-free web query, the user must make an explicit request as in the following code.

~~~python
from aboutmeta import Extract, Path

meta = Extract(Path("/full/path/to/about.yaml"))
meta.build()

meta.validate_urls("project.urls")
~~~
<a id="MULTIMD-TOC-ANCHOR-19"></a>
##### Licences

The licence abbreviations that are taken into account are those provided in the [`SPDX` SPDX License List](https://spdx.org/licenses/) (internally, we use a local version of the [`licenses.json`](https://raw.githubusercontent.com/spdx/license-list-data/main/json/licenses.json) file).
To facilitate data entry, lowercase letters may be used, and hyphens may be replaced with spaces: for example, to indicate the *"Creative Commons Attribution Non Commercial 4.0 International"* licence, it is possible to use `cc by nc 4.0` instead of `CC-BY-NC-4.0` as expected by the `SPDX` project.

> ***NOTE.*** *In the case of an unknown abbreviation, the error message will provide possible suggestions if simple typos have been made in the `YAML` file.*

The digested licence provides the following sub-attributes of ``meta.data.project.licence`.

1. `id` is the standard `SPDX` abbreviation. This text is also used for the basic text version obtained via `str(meta.data.project.licence)` for example.
2. `name` is the full title of the licence.
3. `text` is the text of the licence, which will always be obtained via a web request (you must therefore be connected to obtain this text).

> ***NOTE.*** *You can request that the full text of the licence be added to a file named `LICENCE.txt` located in the folder containing the `about.yaml` file. To do so, use the following code.*

~~~python
from aboutmeta import Extract, Path

meta = Extract(Path("/full/path/to/about.yaml"))
meta.build()

meta.add_licence()
~~~
<a id="MULTIMD-TOC-ANCHOR-20"></a>
##### Languages

You can specify a language using the [ISO 639 standard](https://en.wikipedia.org/wiki/ISO_639), then, if necessary, add a country using the [ISO 3166 standard](https://en.wikipedia.org/wiki/ISO_3166): for example, you can type either `fr` if you do not wish to specify France, or `fr_BE` to indicate Belgian French.

> ***NOTE.*** *The default language is `en_GB` for British English.*

<a id="MULTIMD-TOC-ANCHOR-21"></a>
#### Working with folders and files

The list of paths is validated during digestion and is returned as a list of pairs `(boolean, Path)` that complies with the following specifications.

1. The boolean value is `True` for a path pointing to a file, and `False` for a folder.
2. The path is a `pathlib.Path` object.

> ***NOTE.*** *Paths must point to existing folders and files.*
