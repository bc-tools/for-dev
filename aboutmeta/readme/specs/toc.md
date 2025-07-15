### Working with folders and files

Whether for a document written in small sections or for a monorepo project, it is useful to be able to specify a **list of existing folders and/or files** to explore in a customised order.
The optional `toc` block meets this need. Its content must be a list of relative paths, with folders indicated by a slash ‘/’ at the end of the path, which also serves as a path separator, even when working with the Windows operating system.
Here is a fictitious example.

~~~yaml
toc:
  - relative/path/to/file_1.txt
  - relative/path/to/one/folder/
  - relative/path/inside/one/sub/folder/file_2.md
~~~


When  a folder is specified, this means that it contains an `about.yaml` file that must also be analysed.


> ***NOTE.*** *Using the `Python` module `aboutmeta`, it is possible to specify a default extension, and to check for the validity of all the paths.*
