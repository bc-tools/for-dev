### Minimum requirements

Let’s start with a minimal example of a data type class that only stores height and weight data. This can be done as follows.

~~~python
from aboutmeta.core.data_manager import DataManager


# -------------------------- #
# -- BIOMETRIC DATA CLASS -- #
# -------------------------- #

class Biometric(DataManager):
    yaml_val: str    # Mandatory attribute
    height  : float
    weight  : float


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# Doing tests is the best!
    ...
~~~


Here are the key points regarding attributes.

  1. `DataManager` needs the `yaml_val` attribute to store the user-input data coming from an `about.yaml` file. In our case, this could be `"1m80, 80kg"`, converted to `1.8` and `80.0` by the parser to feed a `Biometric` instance.

  1. `DataManager` exposes the `data_pb` attribute for validation information (see the `validate` method below).


> ***WARNING.*** *Never use the attributes `yaml_val` and `data_pb` to store data!*


Here are the constraints to follow for methods.

  1. `__str__` is managed by the `DataManager` interface to display the `yaml_val` string attribute. **You do not need to implement it.**

  2. The optional `normalize` must be used to normalize data.

  3. The optional `validate` must be used for data validation.


> ***IMPORTANT.*** *Providing a few tests is essential; they will be integrated into the final project's unit test suite.*
