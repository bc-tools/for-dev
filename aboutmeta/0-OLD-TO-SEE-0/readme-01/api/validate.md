### Validate data

Some data, such as file paths, dates, and version numbers, are validated during parsing. Others are only validated upon request, as this requires more in-depth analysis using online tools. For this data, you will need to explicitly request validation. This can be done easily as follows.

~~~python
from aboutmeta import AMData, Path

meta = AMData()
meta.build(yaml_file = Path("/full/path/to/about.yaml"))

if meta.validate():
    print("Valdation OK")

else:
    print(
        "Valdation KO: see all the logging infos in the terminal, "
        "or just the errors in the aboutmeta.log file."
    )
~~~


To simply validate the data in the `YAML` block `project.urls`, just specify the abstract path as follows. In this example, we also request that the log file be deleted before testing the validity of the data.

~~~python
from aboutmeta import AMData, Path

meta = AMData()
meta.build(yaml_file = Path("/full/path/to/about.yaml"))

if meta.validate(
    what      = "project.urls",
    erase_log = True
):
    print('Valdation OK')

else:
    print('Valdation KO!')
~~~


The following sections present the available validations and explain the checks performed.
