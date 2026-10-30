### Post-production tools

Sometimes data requires post-processing actions. For instance, the `about_path` parser needs to build a complete list of absolute paths based on raw paths and/or search patterns (see the snippet below).
By design, only one post-processing step can be defined, which is implemented via the `postprod` function. It must strictly follow one of the signatures below (generic types are shown here for illustration, but you must specify concrete type hints as demonstrated in the snippet below).

  - `postprod(data: object) -> None | dict[str, object]`:
  operate on a single parsed data.

  - `postprod(data: list[object]) -> None | dict[str, object]`:
  operate on a list of parsed data.

  - `(amdata: object, data: object)` and `(amdata: object, data: list[object])` argument signatures:
  require access to instances of `aboutmeta.amdata.AMData`.


What type of data is returned?

  - Returning `None` naturally corresponds to post-processing that strictly interacts with the operating system (such as creating files).

  - Returning a dictionary allows access to specific data via a tag, making it easy to return and retrieve multiple types of nuild data.


> ***NOTE.*** *For returned data, it is strongly recommended to use `Python` constants for tags, following the naming scheme `TAG_{SCHEMA} = '__{SCHEMA}__'` where `{SCHEMA}` is `POSTPROD_<MODULE_NAME>_<DATA_RETURNED>__`. These constants will be integrated automatically into the final product to enhance the user experience.*


> ***CAUTION.*** *As explained in the `parse` function section, never use `from aboutmeta.amdata import AMData`, always type `amdata` as `object`, use `new_instance` method to create new `AMData` instances, and rely on a mock `AMData` class for your tests.*


Here is a real-world use case requiring `aboutmeta.amdata.AMData` instances to analyze `about.yaml` files when folder paths are found.


<!-- PARSER - POSTPROD FUNCTION - START -->

~~~python
# Simplified extract from ''about_path.py'' file (2026-10-31).

TAG_POSTPROD_ABOUT_PATH_FILES = '__POSTPROD_ABOUT_PATH_FILES__'

def postprod(
    amdata: object,
    data  : list[TOCPath]
) -> list[Path]:
    paths = []

# Let's walk!
    for tpath in data:
        ...

# Nothing left to do.
    return {
        TAG_POSTPROD_ABOUT_PATH_FILES: paths,
    }
~~~

<!-- PARSER - POSTPROD FUNCTION - END -->
