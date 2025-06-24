`README.md` piece-by-piece
--------------------------

You can write your `README.md` by typing `MD` chunks. Let's assume we have done this for our fictitious development project `MockProject` which now has the following tree structure.

~~~
+ MockProject
    * about.yaml
    * pyproject.toml
    + changes [...]
    + readme
        * about.md
        * about.yaml
        * cli.md
        * escape.md
        * prologue.md
    + src [...]
    + tests [...]
~~~


The special file `readme/about.yaml` is used here to specify the order in which the different `MD` files are merged. Its contents is as follows where the `toc` key is for *"table of contents"*.

~~~yaml
toc:
  - prologue
  - about
  - mockthis
  - cli
~~~

The construction of the new final product `mockproject` is very simple: we just specify the folder `readme` instead of a file in the `MockProject/about.yaml` file which is now the following one.

''`yaml
dist:
  # We use a relative path with the character /
  # at the end to say that we give a folder.
  readme: readme/
  ignore: |
    tool_*/
    tool_*.*
''`


That's all folks!
