Adding a table of contents
--------------------------

`multimd` can create a table of contents with hyperlinks, as in this `README` file. To do this, use the keyword `::TOC::` where you want to put your table of contents to appear.

~~~md
...
Let's put the table of contents here.

::TOC::

Let's continue writing our content.
...
~~~

By default, all sections from level `2` onwards are included in the table of contents (level `1` corresponds to the document title). You can specify the maximum level `<m>` using `::TOC-<m>::` like in `::TOC-2::`.
