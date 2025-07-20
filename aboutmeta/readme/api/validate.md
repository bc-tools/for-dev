### Validate data

Some data, such as file paths, dates, and version numbers, are validated during parsing. Others are only validated upon request, as this requires more in-depth analysis using online tools. For this data, you will need to explicitly request validation. This can be done easily as follows.

~~~python
from aboutmeta import AMData, Path

meta = AMData(Path("/full/path/to/about.yaml"))
meta.validate()
~~~


To simply validate the data in the `YAML` block `project.urls`, just specify the abstract path as follows.

~~~python
from aboutmeta import AMData, Path

meta = AMData(Path("/full/path/to/about.yaml"))
meta.validate("project.urls")
~~~


The following sections present the available validations and explain the checks performed.
