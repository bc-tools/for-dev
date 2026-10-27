### Derived attributes from mandatory ones

Since `DataManager` inherits from `dataclasses.dataclass`, adding attributes dynamically is not possible to ensure data integrity.
To derive new attributes from initial inputs, use `field(init = False)` for attributes that should not be passed during initialization, and calculate their values within the `__post_init__` method, as shown in the snippet below.


<!-- DERIVATE ATTRS - LICENSING EXTRACT - START -->

~~~python
# Extract of Licensing class code (2026-10-27).

class Licensing(DataManager):
    spdx_id: str
    name   : str = field(init = False)
    url    : str = field(init = False)

    def __post_init__(self) -> None:
        ...
~~~

<!-- DERIVATE ATTRS - LICENSING EXTRACT - END -->
