### From YAML data to internal Python one

Here are the steps to follow.

  1. Start by finding a name to use when asking to `aboutmeta` to invoke your parser. Don't be lacking in inspiration.

  1. The parser name is the `Python` file name where your function for 'digesting' isolated `YAML` data is coded. This function must be named `parse`. Here are **the only possible signatures** for this function (we use generic types for the classes, but you will have to be more precise, as in the accepted parsers).

     + `parse(data: object) -> object` must be used if only data needs to be analyzed, regardless of other of the `about.yaml` file being analyzed.

     + `parse(amdata: object, data: object) -> object` takes into account an instance of the class `aboutmeta.amdata.AMData`. For reference, see the `contrib/parser/code/about_path.py` file.


> ***CAUTION.*** *To prevent circular imports, never use `from aboutmeta.amdata import AMData` when working with `amdata`, which must always be typed as `object`. Unit tests must also work with a mock `AMData` class based on the following one.*

~~~python
class MokeAMData:
    @classmethod
    def new_instance(cls, **kwargs):
        return cls(**kwargs)

    def __init__(
        self,
        flavour: str,
        parent : Path,
    ):
        self.flavour = flavour
        self.parent  = parent

# For post-productions.
        def postprod(
            self,
            keypath: str | list[str],
        ) -> object:
            ...
~~~


> ***IMPORTANT.*** *To build a new instance of `AMData` without importing it, just use the `new_instance` method (it requires the `flavour` and `file` arguments), as in `new_amdata = amdata.new_instance(flavour = ... , file = ...)`.*
