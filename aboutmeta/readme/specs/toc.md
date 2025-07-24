### Working with files

Whether for a document written in small sections or for a monorepo project, it is useful to be able to specify a **list of existing files** to explore in a customised order: the optional `toc` block meets this need. Its content must be a list of paths or patterns.


Here is a fictitious example showing the functionalities available.

~~~yaml
toc:
  - relative/path/to/one/file.txt
  - relative/path/to/one/folder/with/another/toc/
  - glob  : glob/*/pattern/*.md
  - regex : regex/pattern/.*.py
  - r-regex: regex/recursive/search/*.cpp
~~~


> ***IMPORTANT!*** *The search is always done relatively to the folder containing the `about.yaml` file.*
