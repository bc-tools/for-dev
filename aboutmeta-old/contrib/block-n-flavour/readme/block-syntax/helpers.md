### Magic comments

A new block definition must contain a minimum of documentation (these texts will be used as help by the CLI). Here are the situations to be taken into account (using the `project.yaml` file as an example, version August 7, 2025).


#### General block description

The following code shows how to succinctly describe the purpose of the block via a comment at the very beginning of the `YAML` specification file.

~~~yaml
###
# This block allows to describe a project from a technical point
# of view.
###

...
~~~


#### How certain blocks and keys work

After the general description, it is possible - and strongly recommended - to document blocks or keys, but nothing is imposed. Documentation is added in the comments just before the block or key concerned. Here are a few extracts from the `project.yaml` file, where, in the case of the `urls` block, it should be noted that there is no need to document the `home`, `dev` and `issues` keys.

~~~yaml
...

###
# This is the current version number of the project.
###
version*: sem_version

...

###
# Three kinds of URL can be given.
#
#   + ''home'' is for the website of the project, the human one.
#
#   + ''dev'' is dedicated to the repository of the project, this
#     is not intended for human beings.
#
#   + ''issues'' allows regular users to report bugs.
###
urls*:
  home*  : url
  dev*   : .
  issues*: .

...
~~~


#### The special case of alternatives

Documentation of an alternative requires that the various competing keys be documented in sections indicated by magic titles of the form `{key-name}`, as in the following example.

~~~yaml
...

###
# {codename}
# This value, optional for a code-type project, allows to name the
# project differently from the folder containing it.
#
# {doctitle}
# This value is mandatory for a “document” type project: it gives
# the title of the document.
###
codename | doctitle *: . | .

...
~~~
