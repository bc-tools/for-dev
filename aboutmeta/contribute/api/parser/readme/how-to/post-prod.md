### Post-production tools

Sometimes data requires post-processing actions. For instance, the `about_path` parser needs to build a complete list of absolute paths based on raw paths and/or search patterns (see the snippet below).
By design, only one post-processing step can be defined, which is implemented via the `postprod` function. It must strictly follow one of the signatures below (generic types are shown here for illustration, but you must specify concrete type hints as demonstrated in the snippet below).

  - `postprod(data: object) -> object`:
  operate on a single parsed data.

  - `postprod(data: list[object]) -> object`:
  operate on a list of parsed data.

  - `postprod(amdata: object, data: object) -> object` and `postprod(amdata: object, data: list[object]) -> object`:
  require access to an instance of `aboutmeta.amdata.AMData`.


> ***CAUTION.*** *As explained in the `parse` function section, never use `from aboutmeta.amdata import AMData`, always type `amdata` as `object`, use `new_instance` method to create new `AMData` instances, and rely on a mock `AMData` class for your tests.*


Here is a real-world use case requiring `aboutmeta.amdata.AMData` instances to analyze `about.yaml` files when folder paths are found.


<!-- PARSER - POSTPROD FUNCTION -  - START -->

~~~python
# Simplified extract from ''about_path.py'' file (2026-10-27).

def postprod(
    amdata: object,
    data  : list[TOCPath]
) -> list[Path]:
    paths = []

# Let's walk!
    for tpath in data:
        ...
~~~

<!-- PARSER - POSTPROD FUNCTION - END -->
