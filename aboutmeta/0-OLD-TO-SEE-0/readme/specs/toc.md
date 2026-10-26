### Working with files

Whether for a document written in small sections or for a monorepo project, it is useful to be able to specify a **list of existing files** to explore in a customised order: the optional `toc` block meets this need. Its content must be a list of paths or patterns.


Here is a fictitious example showing the functionalities available.

~~~yaml
toc:
# Hard coded file.
  - relative/path/to/one/file.txt
# Hard coded folder with an ''about.yaml'' to follow.
  - relative/path/to/one/folder/with/another/toc/
# Non recursive glob pattern for files.
  - glob: "*.md"
# Recursive glob pattern for files.
  - r-glob: "*.md"
# Non recursive Python regex pattern for files.
  - regex: '.*\.py'
# Recursive Python regex pattern for files.
  - r-regex: '[^/]*\.py'
~~~


> ***IMPORTANT!*** *The search is always done relatively to the folder containing the `about.yaml` file.*
