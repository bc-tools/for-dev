### From YAML data to internal Python one

Here are the steps to follow when building a `Python` data structure from a `YAML` data.

  1.  **Choose a unique parser name.**
  Select a clear and descriptive name that `aboutmeta` will use to invoke your parser.

  1. **Implement the `parse` function.**
  The parser name corresponds to the `Python` filename hosting your `parse` function. This function handles processing isolated `YAML` data and must adhere strictly to one of the following valid signatures (generic types are shown here for illustration, but you must specify concrete type hints as demonstrated in the two snippets below).

     - `parse(data: object) -> object`:
     use this signature when data can be analyzed independently, without requiring context from the rest of the `about.yaml` file.

     - `parse(amdata: object, data: object) -> object`:
     use this signature when access to the `aboutmeta.amdata.AMData` instance is required. See the caution note directly following the snippets.


The following snippet does not require the `aboutmeta.amdata.AMData` instance.


<!-- PARSER - PARSE FUNCTION - NO AMDATA - START -->

~~~python
# Extract from ''sem_version.py'' file (2026-10-27).

def parse(data: str) -> Version:
    try:
        version = VersionInfo.parse(data)

    except ValueError as e:
        raise ParsingError(e)

    return version
~~~

<!-- PARSER - PARSE FUNCTION - NO AMDATA - END -->


This second snippet requires an `aboutmeta.amdata.AMData` instance.


<!-- PARSER - PARSE FUNCTION - WITH AMDATA - START -->

~~~python
# Extract from ''about_path.py'' file (2026-10-27).

def parse(
    amdata: object,
    data  : str
) -> TOCPath:
# No parsing, and all job done by the class
# ''aboutmeta.specs.data.tocpath.TOCPath''.
    return TOCPath(
        spec   = data,
        parent = amdata.parent
    )
~~~

<!-- PARSER - PARSE FUNCTION - WITH AMDATA - END -->


> ***CAUTION.*** *To prevent circular imports, never use `from aboutmeta.amdata import AMData` when working with `amdata`, which must always be typed as `object`. Tests must also work with a mock `AMData` class based on the example below, where the `new_instance` method allows creating a new `AMData` instance without importing it (note that `new_instance` and `postprod` are actual `AMData` methods).*


<!-- PARSER - MOKE MADATA - START -->

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

# Only for post-processing features.
        def postprod(
            self,
            keypath: str | list[str],
        ) -> object:
            ...
~~~

<!-- PARSER - MOKE MADATA - END -->
