Finishing touches
-----------------

### What is done automatically

During final formatting, `multimd` standardises the source code to prevent `git` from spotting any *'false'* changes. Here's what happens behind the scenes.

  1. **Add a table of contents**, with hyperlinks, via the alias `::TOC::` that can be used **only on one line and only once**. See the following section for more details.

  1. **Section titles** use the non-standard, but very visual, syntax of `===` and `---` for the first two levels of section, and then the `#` symbol is used.

  1. **Removal of unnecessary spaces**.

  1. **Management of consecutive blank lines**: excluding formatted code, consecutive blank lines are reduced to a single one, except before section headings, where they are doubled, except for a heading just after another. Did you understand that sentence? I don't really. `:-)`

  1. **Add a blank line** after an `MD` block, if necessary.


> ***NOTE.*** The `Python` API allows you to apply the above normalisation to an `MD` file of your choice, as in the following code where `Path` is the class provided by the `pathlib` module (it is possible to use the same source and destination).

~~~python
from multimd import finalize, Path

stdit(
    src  = Path("/full/path/to/MY-FILE.md")
    dest = Path("/full/path/to/MY-FILE-STD.md")
)
~~~


### ToC settings

In the following code, the alias `::TOC::` will be replaced by a table of contents, with hyperlinks, in the final document.

~~~md
...
My project
==========

Let's put *the table of contents here*.

::TOC::

Let's continue writing **our content**.
...
~~~

By default, all sections from level `2` onwards are included in the table of contents (level `1` corresponds to the document title). You can specify the maximum level `<m>` of sections to be retained using `::TOC-<m>::`, as in `::TOC-2::`, which requests that only sections of level `2` be retained.
