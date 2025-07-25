<!----------------------------------------------------------------
  -- File created by the ''multimd'' project, version 1.0.0.    --
  --                                                            --
  -- ''multimd'', soon to be available on PyPI, is developed at --
  -- https://github.com/bc-tools/for-dev/tree/main/multimd      --
  ---------------------------------------------------------------->


The Python module aboutmeta
===========================

This document is a complete tutorial showing all the available features.

**Table of contents**

<a id="MULTIMD-GO-BACK-TO-TOC"></a>
- [What is aboutmeta?](#MULTIMD-TOC-ANCHOR-0)
- [Complete list of dependencies](#MULTIMD-TOC-ANCHOR-1)
- [YAML specifications](#MULTIMD-TOC-ANCHOR-2)
    - [The project itself](#MULTIMD-TOC-ANCHOR-3)
        - [Version](#MULTIMD-TOC-ANCHOR-4)
        - [Date](#MULTIMD-TOC-ANCHOR-5)
        - [Project identity.](#MULTIMD-TOC-ANCHOR-6)
        - [Developers, authors and contributors](#MULTIMD-TOC-ANCHOR-7)
        - [URLs of the project](#MULTIMD-TOC-ANCHOR-8)
        - [Licenses](#MULTIMD-TOC-ANCHOR-9)
        - [Languages](#MULTIMD-TOC-ANCHOR-10)
        - [Technologies required](#MULTIMD-TOC-ANCHOR-11)
        - [Keywords](#MULTIMD-TOC-ANCHOR-12)
    - [Working with files](#MULTIMD-TOC-ANCHOR-13)
        - [Direct paths](#MULTIMD-TOC-ANCHOR-14)
        - [glob patterns](#MULTIMD-TOC-ANCHOR-15)
        - [regex patterns](#MULTIMD-TOC-ANCHOR-16)
- [The Python API](#MULTIMD-TOC-ANCHOR-17)
    - [Data extraction](#MULTIMD-TOC-ANCHOR-18)
    - [Use of data](#MULTIMD-TOC-ANCHOR-19)
        - [The project itself](#MULTIMD-TOC-ANCHOR-20)
            - [Version](#MULTIMD-TOC-ANCHOR-21)
            - [Date](#MULTIMD-TOC-ANCHOR-22)
            - [Developers, authors and contributors](#MULTIMD-TOC-ANCHOR-23)
            - [Licenses](#MULTIMD-TOC-ANCHOR-24)
            - [Languages](#MULTIMD-TOC-ANCHOR-25)
        - [Working with folders and files](#MULTIMD-TOC-ANCHOR-26)
    - [Validate data](#MULTIMD-TOC-ANCHOR-27)
        - [Affiliation](#MULTIMD-TOC-ANCHOR-28)
        - [Email](#MULTIMD-TOC-ANCHOR-29)
        - [URL](#MULTIMD-TOC-ANCHOR-30)

<a id="MULTIMD-TOC-ANCHOR-0"></a>
What is aboutmeta? <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
------------------

This project allows metadata to be defined in `about.yaml` files, making it easier for third-party programs to manage digital projects (code projects and document-type projects).

> ***NOTE.*** *A digital project is simply a folder containing content, some of which is only useful during development (tools and tests), while other content is used to create the final product (a computer program or a document to read). In other word, `aboutmeta` is agnostic.*

<a id="MULTIMD-TOC-ANCHOR-1"></a>
Complete list of dependencies <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
-----------------------------

Here are the `Python` libraries used by `aboutmeta`. Version numbers are indicated in brackets.

- `email_validator` **[2.2]**
- `langcodes` **[3.5]**
- `natsort` **[8.4]**
- `python-box` **[7.3]**
- `pyyaml` **[6.0]**
- `rapidfuzz` **[3.13]**
- `requests` **[2.32]**
- `rich` **[13.9]**
- `semver` **[3.0]**

<a id="MULTIMD-TOC-ANCHOR-2"></a>
YAML specifications <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
-------------------

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
2. A virtual pointed path like `block-3.key-1` refers to the key `key-1` of the block `block-3`.
3. Optional attributes will be indicated by their name followed by an asterisk `*`.
4. Sometimes, an attribute can be used either in the singular or plural form, but not both at the same time. In this case, the name will end with `(s)`, as in `author(s)`.

> ***NOTE.*** *If you are unfamiliar with the general syntax of `YAML`, the [Wikipedia article YAML](https://wikipedia.org/wiki/YAML) is a good place to start.*

---

> ***IMPORTANT.*** *Technically, `YAML` files are read securely by treating all values as simple character strings.*

<a id="MULTIMD-TOC-ANCHOR-3"></a>
### The project itself <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Let's start with a complete description of a fictional code project.

~~~yaml
project*:
  version*: 0.0.0-beta.1
  date*   : 2025-06-27

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

  licenses*:
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

<a id="MULTIMD-TOC-ANCHOR-4"></a>
#### Version <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The optional `project.version` key allows to specify a version number that complies with ["Semantic Versioning"](https://semver.org/), such as `1.0.0`, `0.0.0-beta.1`, and `0.3.1-beta.1+build.5`.

<a id="MULTIMD-TOC-ANCHOR-5"></a>
#### Date <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The optional `project.date` key allows to give a date in the English format `YYYY-MM-DD` like `2025-07-15`.

<a id="MULTIMD-TOC-ANCHOR-6"></a>
#### Project identity. <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The keys `project.acronym`, `project.codename`, `project.doctitle`, and `project.desc` are used to quickly identify a project.

> ***IMPORTANT.*** *The key `desc` is mandatory.*

> ***WARNING!*** *`codename` and `doctitle` can never be used at the same time.*

Here is how these different keys are used.

1. `desc` is used to quickly describe the project.
2. `acronym` explains the origin of an acronym: for example, `"[@]bout [Desc]ription"` explains the choice for the project name `@Desc`.
3. `codename` allows you to specify the name of a code-type project if it differs from that of the project folder.
4. `doctitle` must be used for a document-type project. This is because such a project must have a title.

> ***NOTE.*** *The last two points show that `aboutmeta` will assume that it is working with a code-type project by default.*

<a id="MULTIMD-TOC-ANCHOR-7"></a>
#### Developers, authors and contributors <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The keys `project.author`, which is mandatory, and `project.contrib`, which is optional, are used either in the singular form to indicate a single person, or in the plural form to indicate a list of people. Here is a fictitious use case.

~~~yaml
project:
  author: Ada, Lovelace

  contribs:
    - Alan, Turing
    - Donald, Knuth
~~~

The following forms of personal identification are managed.

1. **Title (mandatory):** `Surname`, `First name, Compound surname`, `First name 1, First name 2, Long surname`... Hereinafter, we will refer to one of the above forms as `<title>`.
2. **Email address (optional):** `<title> [one.id@provider.abc]` uses square brackets for the email.
3. **Affiliation (optional):** `<title> (Name of institute, Country)` uses parentheses for the affiliation.
4. **Indicate everything:** only the format `<title> [email] (institute)` is allowed.

> ***NOTE.*** *Emails are not verified, but they can be validated on demand (technically, this requires an internal connection, so it is not possible to validate an email every time an `about.yaml` file is analyzed).*

<a id="MULTIMD-TOC-ANCHOR-8"></a>
#### URLs of the project <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The optional `project.url` block allows to provide hyperlinks via the following keys, all of which are optional.

1. `home` allows to specify the address of a website dedicated to the project.
2. `dev` is used to point to a repository for managing project development.
3. `issues` redirects users to the page where they can report bugs or make suggestions.

> ***NOTE.*** *URLs are not verified, but they can be validated on demand (technically, this requires an internal connection, so it is not possible to validate a URL every time an `about.yaml` file is analyzed).*

<a id="MULTIMD-TOC-ANCHOR-9"></a>
#### Licenses <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The optional block `project.licenses` is used to indicate licenses via the following keys.

1. `code` is for the license of the code or document relating to the project.
2. `manual` allows, in the case of a code-type porject, the selection of a license specific to the user manual.

The license names proposed by the [`SPDX` SPDX License List](https://spdx.org/licenses/) are taken into account, with a certain degree of flexibility: for example, you can type `gpl 3.0+` and `cc by nc 4.0` instead of `GPL-3.0+` and `CC-BY-NC-4.0`.

<a id="MULTIMD-TOC-ANCHOR-10"></a>
#### Languages <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The optional `project.langs` block allows to specify the languages used for the following parts of a code-type project.

1. The `doc` key is for the language used to write the technical documentation.
2. The `manual` key is for the language used to write the user manual.

You can specify a language using the [ISO 639 standard](https://en.wikipedia.org/wiki/ISO_639), then, if necessary, add a country using the [ISO 3166 standard](https://en.wikipedia.org/wiki/ISO_3166): for example, you can type either `fr` if you do not wish to specify France, or `fr-BE` to indicate Belgian French.

> ***NOTE.*** *The default language is `en-US` for US English.*

> ***TIP.*** *You can use `_` instead of `-`. This can be useful when pasting external text.*

<a id="MULTIMD-TOC-ANCHOR-11"></a>
#### Technologies required <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Using the optional `project.require` block, it is possible to provide a list of programming languages required for the code to work, or for compiling a document, this depends on the type of project.
For the record, we reproduce the fictitious example presented at the beginning of this document.

~~~yaml
project:
  require:
    - python3
    - latex
~~~
<a id="MULTIMD-TOC-ANCHOR-12"></a>
#### Keywords <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Keywords are used to categorise the type of project succinctly: this is done via the optional `project.keywords` key. Here is the example we proposed at the beginning of the document.

~~~yaml
project:
  keywords:
    - metadata
    - coding
    - writing
~~~
<a id="MULTIMD-TOC-ANCHOR-13"></a>
### Working with files <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Whether for a document written in small sections or for a monorepo project, it is useful to be able to specify a **list of existing files** to explore in a customised order: the optional `toc` block meets this need. Its content must be a list of paths or patterns.

Here is a fictitious example showing the functionalities available.

~~~yaml
toc:
# Hard coded file.
  - relative/path/to/one/file.txt
# Hard coded folder with an ''about.yaml'' to follow.
  - relative/path/to/one/folder/with/another/toc/
# Non recursive glob pattern for files.
  - glob: "*.md"
# Recursive glob pattern for files.
  - r-glob: "*.md"
# Non recursive Python regex pattern for files.
  - regex: '.*\.py'
# Recursive Python regex pattern for files.
  - r-regex: '[^/]*\.py'
~~~
> ***IMPORTANT!*** *The search is always done relatively to the folder containing the `about.yaml` file.*

<a id="MULTIMD-TOC-ANCHOR-14"></a>
#### Direct paths <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

You can use a verbatim relative path of either a file, or a folder, with folders indicated by a slash `/` at the end of the path (the slash `/` also serves as a path separator, even when working with the Windows operating system).

> ***CAUTION!*** *When a folder is specified, it must contain an `about.yaml` file with a `toc` block to be analyzed by `aboutmeta`.*

> ***NOTE.*** *If you want to choose the files kept inside a folder without using an `about.yaml` file, you will have to use a pattern as explained in the upcoming sections.*

<a id="MULTIMD-TOC-ANCHOR-15"></a>
#### glob patterns <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The `glob` patterns are simply indicated using something like `glob: "*.md"`, or `r-glob: "*.md"` if you need a recursive search.

<a id="MULTIMD-TOC-ANCHOR-16"></a>
#### regex patterns <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

A `regex` pattern can be either, for example, `regex: '[^/]*\.md'`, or `r-regex: '[^/]*\.md'` for a recursive search.

> ***WARNING!*** *In a `YAML` file, using single quotation marks avoids escaping backslashes. With double quotation marks, we would have had to type `"[^/]*\\.py"` which is less user-friendly.*

<a id="MULTIMD-TOC-ANCHOR-17"></a>
The Python API <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
--------------

In addition to providing `YAML` specifications, that can be used in your preferred programming language, `aboutmeta` offers a `Python` module based on a plugin system that handles certain data formats.
The following sections describe what is available in the current version.

> ***NOTE.*** *The `contrib/parser` folder contains a `README.md` file explaining how to easily build and suggest new parsers.*

<a id="MULTIMD-TOC-ANCHOR-18"></a>
### Data extraction <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The analysis of an `about.yaml` file is done simply as follows where `Path` is the class from the `pathlib` module.

~~~python
from aboutmeta import AMData, Path

meta = AMData()

meta.build(yaml_file = Path("/full/path/to/about.yaml"))
~~~

If necessary, and this is used internally by `aboutmeta`, you can specify the main blocks to be analysed. For example, to focus on the `toc` block, simply do the following, where `SET_KEEP_ONLY_TOC = set([‘toc’])` is provided by `aboutmeta`.

~~~python
meta.build(
    yaml_file = Path("/full/path/to/about.yaml"),
    keep      = SET_KEEP_ONLY_TOC
)
~~~
> ***NOTE.*** *By default, `aboutmeta` uses `SET_KEEP_ALL` which is the set of all the main blocks.*

<a id="MULTIMD-TOC-ANCHOR-19"></a>
### Use of data <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Once the data has been extracted by `aboutmeta.AMData`, the `data` attribute of the `meta` object, see the previous section, provides access to the digested data in a simple manner.

1. If we take the example given in the specifications, access to the home URL is done via `meta.data.project.urls.home`, which is ideal for non-dynamic code.
2. For dynamic coding, it is possible to use a virtual pointed path as in `meta("project.urls.home")` with parentheses instead of square brackets.

The following sections present the data after digestion.

> ***NOTE.*** *To keep things simple, we will always use access to data processed via the `data` attribute, and work with the `meta` object showed in the previous section.*

> ***TIP.*** *To retrieve a standard version of the original `YAML` piece of data, just use the string version of the corresponding `Python` data as in `str(meta.verbatim.project.date)`.*

<a id="MULTIMD-TOC-ANCHOR-20"></a>
#### The project itself <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

We only present digested data that does not reproduce the contents of the `YAML` file as string data.

> ***NOTE.*** *The next sections will use the abbreviation `mdp = meta.data.project`.*

<a id="MULTIMD-TOC-ANCHOR-21"></a>
##### Version <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Let's assume that the `YAML` file contains the data `version: 1.2.3-beta.4+build.5`. By default, the digest will provide the following information.

1. The full version number is accessible via `str(mdp.version)`.
2. `mdp.version.major` provides the integer `1`.
3. `mdp.version.minor` provides the integer `2`.
4. `mdp.version.patch` provides the integer `3`.
5. `mdp.version.prerelease` provides the text `beta.4`.
6. `mdp.version.build` provides the text `build.5`.

> ***NOTE*** *Behind the scenes, the version number data is a `semver.version.Version` object which has useful methods. For example, `mdp.version.next_version(part="prerelease")` gives the version `1.2.3-beta.5` with our example above.*

<a id="MULTIMD-TOC-ANCHOR-22"></a>
##### Date <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The date is accessible via the attribute `mdp.date`.

1. The full date is obtained using `str(mdp.date)`
2. `mdp.year` provides the integer value of the year.
3. `mdp.month` provides the integer number of the month.
4. `mdp.day` provides the integer number of the day.

> ***NOTE*** *Behind the date data is a `datetime.date` object (which provides access to all the methods associated with these type of object).*

<a id="MULTIMD-TOC-ANCHOR-23"></a>
##### Developers, authors and contributors <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

In the `YAML` file, the singular forms `project.author` and `project.contrib` will produce a single data object, while the plural forms `project.authors` and `project.contribs` will produce a list of instances of `aboutmeta.person.Person` that have the following attributes.

1. `firstnames` is the list of first names.
2. `surname` is the surname.
3. `email` is to the text written in parentheses.
4. `affiliation` is to the text written in square brackets.

<a id="MULTIMD-TOC-ANCHOR-24"></a>
##### Licenses <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The license abbreviations taken into account are those provided in the [`SPDX` SPDX License List](https://spdx.org/licenses/) (internally, we use a local version of the [`licenses.json`](https://raw.githubusercontent.com/spdx/license-list-data/main/json/licenses.json) file), and that are not deprecated.
To facilitate data entry, lowercase letters may be used, and hyphens may be replaced with spaces: for example, to indicate the *"Creative Commons Attribution Non Commercial 4.0 International"* license, it is possible to use `cc by nc 4.0` instead of `CC-BY-NC-4.0` as expected by the `SPDX` project.

> ***NOTE.*** *In the case of an unknown abbreviation, the error message can indicate possible suggestions if simple typos have been made in the `YAML` file.*

The digested license provides the following information.

1. `mdp.license.std` is the standard `SPDX` abbreviation. This text is also used for the basic text version obtained via `str(mdp.license)` for example.
2. `mdp.license.name` is the full title of the license.
3. `mdp.license.ref` is a URL pointed to the `SPDX` web page describing the license.

<a id="MULTIMD-TOC-ANCHOR-25"></a>
##### Languages <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

A digested language provides the following information in the case of the technical documentation, but the same is true for other contextes.

1. `mdp.langs.doc.std` is the standard full identifier: for example, `fr` becomes `fr-FR`. This text is also used for the basic text version obtained via `str(mdp.langs.doc)`.
2. `mdp.langs.doc.name` is the English name of the language.
3. `mdp.langs.doc.territory` is the English name of the territory associated with the language.

<a id="MULTIMD-TOC-ANCHOR-26"></a>
#### Working with folders and files <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The paths and patterns are validated during parsing, and a list of `pathlib.Path` objects pointing to files is returned (the absolute paths are used).

<a id="MULTIMD-TOC-ANCHOR-27"></a>
### Validate data <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

Some data, such as file paths, dates, and version numbers, are validated during parsing. Others are only validated upon request, as this requires more in-depth analysis using online tools. For this data, you will need to explicitly request validation. This can be done easily as follows.

~~~python
from aboutmeta import AMData, Path

meta = AMData(Path("/full/path/to/about.yaml"))
meta.build()

if meta.validate():
    print("Valdation OK")

else:
    print(
        "Valdation KO: see all the logging infos in the terminal, "
        "or just the errors in the aboutmeta.log file."
    )
~~~

To simply validate the data in the `YAML` block `project.urls`, just specify the abstract path as follows. In this example, we also request that the log file be deleted before testing the validity of the data.

~~~python
from aboutmeta import AMData, Path

meta = AMData(Path("/full/path/to/about.yaml"))
meta.build()

if meta.validate(
    what      = "project.urls",
    erase_log = True
):
    print('Valdation OK')

else:
    print('Valdation KO!')
~~~

The following sections present the available validations and explain the checks performed.

<a id="MULTIMD-TOC-ANCHOR-28"></a>
#### Affiliation <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The validity test for affiliation to an organization or company is based simply on the `OpenStreetMap` API.

<a id="MULTIMD-TOC-ANCHOR-29"></a>
#### Email <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

For an email, the following validity tests are performed.

1. Is the email syntax correct?
2. Does the email domain name exist?

<a id="MULTIMD-TOC-ANCHOR-30"></a>
#### URL <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

For a URL, the following tests are performed during validation.

1. Is the domain name of the URL stored in a DNS service?
2. Is an “empty content” HTTP request detected?
