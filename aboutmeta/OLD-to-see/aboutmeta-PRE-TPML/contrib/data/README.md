<!----------------------------------------------------------------
  -- File created by the ''multimd'' project, version 1.0.0.    --
  --                                                            --
  -- ''multimd'', soon to be available on PyPI, is developed at --
  -- https://github.com/bc-tools/for-dev/tree/main/multimd      --
  ---------------------------------------------------------------->


Add new data objects
====================

**Table of contents**

<a id="MULTIMD-GO-BACK-TO-TOC"></a>
- [Structure of the "contrib/data-obj" folder](#MULTIMD-TOC-ANCHOR-0)
    - [The changes folder](#MULTIMD-TOC-ANCHOR-1)
    - [The status folder](#MULTIMD-TOC-ANCHOR-2)
    - [The code folder](#MULTIMD-TOC-ANCHOR-3)
- [How to propose a new data object?](#MULTIMD-TOC-ANCHOR-4)
    - [Minimum requirements](#MULTIMD-TOC-ANCHOR-5)
    - [Normalize a `YAML` data](#MULTIMD-TOC-ANCHOR-6)
    - [Validate a data parsed](#MULTIMD-TOC-ANCHOR-7)

<a id="MULTIMD-TOC-ANCHOR-0"></a>
Structure of the "contrib/data-obj" folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
------------------------------------------

<a id="MULTIMD-TOC-ANCHOR-1"></a>
### The changes folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This folder is just a communication tool between contributors to indicate important changes.

<a id="MULTIMD-TOC-ANCHOR-2"></a>
### The status folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This folder allows you to know the status of your proposal. Its structure mimics the folder of contributions: `YAML` files correspond to contribution files.

<a id="MULTIMD-TOC-ANCHOR-3"></a>
### The code folder <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

This folder contains all the data object codes.

<a id="MULTIMD-TOC-ANCHOR-4"></a>
How to propose a new data object? <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>
---------------------------------

Before adding a new data type class, make sure that a ready-made solution does not already exist. For reference, see the approaches used by the `date` and `sem_version` parsers.
If no reliable and well-established solution is available, the new data type class must comply with the rules described in the following sections.

<a id="MULTIMD-TOC-ANCHOR-5"></a>
### Minimum requirements <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

At the very least, your class must be structured as follows.

~~~python
from dataclasses  import dataclass

from aboutmeta.core.dataprinter import DataPrinter


# ------------------- #
# -- MY DATA CLASS -- #
# ------------------- #

@dataclass(frozen = True)
class MyDataClass(DataPrinter):
    ...
~~~

Let's explain these technical choices.

1. `@dataclass(frozen = True)` is used to make the data produced by a parser immutable.
2. The `std` attribute must always be present, and it is managed by the `DataPrinter` class. This attribute is a **standardized version** of the data extracted from the `about.yaml` file, the construction of this standardized value being **the responsibility of the parser**.
3. The `DataPrinter` interface implements the `__str__` magic method, which just prints the string attribute `std`.

Of course, it is entirely possible to add other attributes or methods to the class *(see `license.License` for an example of use)*. However, **the following methods are special ones**.

1. `__str__` is handled by the `DataPrinter` interface. **You don't have to implment it!**
2. `normalized` is needed to normalize some data.
3. `validate` is used for validation processes.

> ***NOTE.*** *The following sections explain how to implement the special methods `normalized` and `validate`.*

<a id="MULTIMD-TOC-ANCHOR-6"></a>
### Normalize a `YAML` data <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The special zero-argument method `normalized` must return a string **normalized** version of the `std` attribute, **without modifying any attributes**. This method is used in rare cases where initial normalization is not straightforward: the `url.URl` class is a good example of a practical case.

> ***IMPORTANT.*** *The normalization process must be 100% reliable, even if its main use will be during terminal sessions.*

<a id="MULTIMD-TOC-ANCHOR-7"></a>
### Validate a data parsed <a href="#MULTIMD-GO-BACK-TO-TOC" style="text-decoration: none;"><span style="margin-left: 0.25em; font-weight: bold; position: relative; top: -.5pt;">&#x2191;</span></a>

The special zero-argument method `validate` is used to validate a data. It must return the number of problem found, and each problem found should be indicated using a log communication: see the `url.URL` class for a concrete example of its use.

> ***IMPORTANT.*** *As not all validation processes are considered 100% reliable, the `validate` method is only useful for terminal sessions.*
