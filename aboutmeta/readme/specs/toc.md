### Organising folders and files

Whether for a document written in small sections or for a monorepo project, it is useful to be able to specify a list of folders and files to explore in a customised order.
The optional `toc` block meets this need. Its content must be a list of relative paths, with folders indicated by a slash ‘/’ at the end of the path, which also serves as a path separator, even when working with the Windows operating system.
Here is a fictitious example.

~~~yaml
toc:
  - relative/path/to/file_1
  - relative/path/to/one/folder/
  - relative/path/inside/one/sub/folder/file_2
~~~
