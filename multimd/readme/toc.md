Adding a table of contents and standard formatting
--------------------------------------------------

XXXX

`multimd` can create a table of contents with hyperlinks, as in this `README` file. To do this, use the keyword `::TOC::` where you want to put your table of contents to appear.

~~~md
...
Let's put the table of contents here.

::TOC::

Let's continue writing our content.
...
~~~

By default, all sections from level `2` onwards are included in the table of contents (level `1` corresponds to the document title). You can specify the maximum level `<m>` of sections to be retained using `::TOC-<m>::`, as in `::TOC-2::`.


> ***NOTE.*** There is also an easy-to-use `Python` API where `Path` is the class from the `pathlib` module.

~~~python
from multimd import finalize, Path

finalize(Path("/full/path/to/README.md"))
~~~
