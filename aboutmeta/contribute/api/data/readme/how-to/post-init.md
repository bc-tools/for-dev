### Derived attributes from mandatory ones

Since `DataManager` inherits from `dataclasses.dataclass`, adding attributes dynamically is not possible (which has the advantage of ensuring data intergity). How can you derive new attributes from the initially provided data? The approach is straightforward, as shown in the following code snippet, where `field(init = False)` is used to indicate an attribute that does not need to be provided during `DataManager` initialization, while the `__post_init__` method computes these new attributes.

~~~python
# Extract of License class code.
# Version 2026-10-19

class License(DataManager):
    spdx_id: str
    name   : str = field(init = False)
    url    : str = field(init = False)

    def __post_init__(self) -> None:
        ...
~~~
