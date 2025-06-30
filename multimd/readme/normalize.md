Finishing touches
-----------------

### What is done automatically?

During final formatting, `multimd` standardises the source code to prevent `git` from spotting any *'false-positive'* changes. Here's what happens behind the scenes.

  1. **Add a table of contents**, with hyperlinks, via the alias `::TOC::` that can be used **only alone on one line and only once**. See the following section for more details.

  1. **Section titles** use the non-standard, but very visual, syntax of `===` and `---` for the first two levels of section, and then consecutive `#` symbols are used.

  1. **Removal of unnecessary spaces**.

  1. **Management of consecutive blank lines**: excluding formatted code, consecutive blank lines are reduced to a single one.

  1. **Add a blank line** after an `MD` block, if necessary.


### ToC settings

In the following code, the alias `::TOC::` will be replaced by a full table of contents, with hyperlinks, in the final document. In fact, the first level `1` heading is never added, as it is the title of the document.

~~~md
...
My project
==========

Let's put *the table of contents here*.

::TOC::

Let's continue writing **our content**.
...
~~~

By default, all sections from level `2` onwards are included in the table of contents (level `1` corresponds to the document title). You can specify the maximum depth `<depth>` of the table of content sections to be retained using `::TOC-<depth>::`.

  * `::TOC-1::` requests that only sections of level `2` are retained.

  * `::TOC-2::` requests that only sections of level `2` or `3` are retained.
