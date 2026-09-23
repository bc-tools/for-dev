### Minimum requirements

Let’s start with a minimal example of a data type class that only stores height and weight data. This can be done as follows.

~~~python
from aboutmeta.core.data_manager import DataManager


# -------------------------- #
# -- BIOMETRIC DATA CLASS -- #
# -------------------------- #

class Biometric(DataManager):
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

  1. `aboutmeta.core.data_manager.DataManager` uses the `std_value` attribute to store a standard user-input data coming from an `about.yaml` file. In our case, this could be `"1m80, 80kg"`, converted to `1.8` and `80.0` by the parser to feed a `Biometric` instance.

  1. `aboutmeta.core.data_manager.DataManager` is an abstract class that produces frozen classes using `@dataclass(frozen=True)`.


> ***WARNING.*** *Never use the `std_value` attribute to store data!*


Here are the methodological constraints to follow.

  1. `__str__` is managed by the `DataManager` interface to display the `std_value` string attribute. **You do not need to implement it.**

  2. The optional `normalize` normalizes data.

  3. The optional `validate` handles data validation logic.


> ***NOTE:*** You can, of course, add additional methods to the class if needed *(see the methode `add_license` of `license.License` for an example)*.
