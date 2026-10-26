### Data extraction

The analysis of an `about.yaml` file is done simply as follows where `Path` is the class from the `pathlib` module.

~~~python
from aboutmeta import AMData, Path

meta = AMData()

meta.build(yaml_file = Path("/full/path/to/about.yaml"))
~~~


If necessary, and this is used internally by `aboutmeta`, you can specify the main blocks to be analysed. For example, to focus on the `toc` block, simply do the following, where `SET_KEEP_ONLY_TOC = set([‘toc’])` is provided by `aboutmeta`.

~~~python
meta.build(
    yaml_file = Path("/full/path/to/about.yaml"),
    keep      = SET_KEEP_ONLY_TOC
)
~~~


> ***NOTE.*** *By default, `aboutmeta` uses `SET_KEEP_ALL` which is the set of all the main blocks.*
