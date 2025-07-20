### Working with folders and files

Whether for a document written in small sections or for a monorepo project, it is useful to be able to specify a **list of existing folders and/or files** to explore in a customised order.
The optional `toc` block meets this need. Its content must be a list of relative paths, with folders indicated by a slash `/` at the end of the path, which also serves as a path separator, even when working with the Windows operating system.
Here is a fictitious example.

~~~yaml
toc:
  - relative/path/to/file_1.txt
  - relative/path/to/one/folder/
  - relative/path/inside/one/sub/folder/file_2.md
~~~


When a subfolder is specified, the search is performed as follows.

  1) Either an `about.yaml` file is present in the subfolder, in which case `aboutmeta` analyzes its `toc` block.

  1) Otherwise, all files present in the subfolder will be retrieved and sorted in a "natural" way.
