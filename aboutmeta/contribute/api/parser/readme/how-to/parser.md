### How to propose a new parser?

Here are the steps to follow.

  1. Start by finding a name to use when asking to `aboutmeta` to invoke your parser. Don't be lacking in inspiration.

  1. The name you choose is the name of the `Python` file where your function for 'digesting' isolated data is coded. This function must be named `parse`. Here are **the only possible signatures** for this function (here, we use generic types for the classes, but you will have to be more precise, as in the accepted parsers).

     + `parse(data: str) -> object` must be used if only data is to be analyzed, regardless of other of the `about.yaml` file being analyzed.

     + `parse(amdata_cls: object, data: str) -> object` also takes into account the class `aboutmeta.amdata.AMData` to be instanciated. See the next section 'How to add a post-production tool?'.

  1. Specific parsing errors must be handled to allow for user input errors (cf CLI and logging communications). This needs the use of `aboutmeta.core.errors.ParsingError` exception class. **It is best to use `from aboutmeta.data.errors import ParsingError`.**

  1. You can add other processing functions necessary for the operation of your parser, provided that you do not use the name `map_list`, which is reserved for processing parsed data lists as explained in the 'How to add a post-production tool?' section.
