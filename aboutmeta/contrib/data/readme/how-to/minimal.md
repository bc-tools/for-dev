### Minimum requirements

At the very least, your class must be structured as follows. We imagine here that no tests are needed.

~~~python
from dataclasses  import dataclass

from aboutmeta.core.dataprinter import DataPrinter


# ------------------- #
# -- MY DATA CLASS -- #
# ------------------- #

@dataclass(frozen = True)
class MyDataClass(DataPrinter):
    ...


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Nothing to test!
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
