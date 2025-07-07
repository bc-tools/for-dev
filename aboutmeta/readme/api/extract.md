### Data extraction

The analysis of an `about.yaml` file is done simply as follows where `Path` is the class from the `pathlib` module.

~~~python
from aboutmeta import AboutMeta, Path

meta = AboutMeta(Path("/full/path/to/about.yaml"))
meta.build()
~~~
