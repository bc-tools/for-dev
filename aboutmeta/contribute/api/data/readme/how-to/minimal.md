### Minimum requirements

Let’s start with a minimal example of a data type class that only stores height and weight data. This is done as follows.

~~~python
from aboutmeta.core.dataprinter import DataPrinter


# -------------------------- #
# -- BIOMETRIC DATA CLASS -- #
# -------------------------- #

class Biometric(DataPrinter):
    height: float
    weight: float


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Doing tests is the best!
    ...
~~~


Here are the key points regarding attributes.

  1. `aboutmeta.core.dataprinter.DataPrinter` uses the `XXX` attribute to store user-input data coming from an `about.yaml` file. In our case, this could be `"1m80, 80kg"`, converted to `1.8` and `80.0` by the parser.

  1. `aboutmeta.core.dataprinter.DataPrinter` is an abstract class that produces a frozen instance using `@dataclass(frozen=True)`.


> ***WARNING.*** *Never use the `XXX` attribute to store data!*


Here are the methodological constraints to follow.

  1. `__str__` is managed by the `DataPrinter` interface to display the `XXX` string attribute. **You do not need to implement it.**

  2. The optional `normalize` normalizes the `XXX` string attribute.

  3. The optional `validate` handles data validation logic.


> ***NOTE:*** You can, of course, add additional methods to the class if needed *(see `license.License` for an example)*.
