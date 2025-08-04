### Minimum requirements

At the very least, your class must be structured as follows.

~~~python
from dataclasses  import dataclass

from aboutmeta.core.dataprinter import *

@dataclass(frozen = True)
class MyDataClass(DataPrinter):
    std : str
~~~


Let's explain thos technical choices.

  1. `@dataclass(frozen = True)` is used to make the data produced by a parser immutable.

  2. The `std` attribute must always be present. It contains a **standardized version** of the data extracted from the `about.yaml` file.
  The construction of this standardized value is **the responsibility of the parser**.

  3. The `DataPrinter` interface implements only the `__str__` magic method, which prints the string attribute `std`.


Of course, it is entirely possible to add other attributes or methods to the class.
However, **additional methods must not be named** `__str__`, as this is handled by `DataPrinter`, and methods `normalize` or `validate` because they are special ones (see the following sections): see the `license.License` class for a concrete example of its use.
