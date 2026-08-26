### Magic comments

A new block definition must contain a minimum of documentation (these texts will be used as help by the CLI and in documentaion).


#### General block description

The following code shows how to succinctly describe the purpose of the block via a comment at the very beginning of the `YAML` specification file.

~~~yaml
###
# This 1st comment **must** describe the block from
# a technical point of view.
###

# Next comes the content of the file.
~~~


#### How certain blocks and keys work

After the general description, it is possible - and strongly recommended - to document blocks or keys, but nothing is imposed. Documentation is added in the comments just before the block or key concerned. Here are a few extracts from the `project.yaml` file, where, in the case of the `urls` block, it should be noted that the `home`, `dev`, and `issues` keys are not documented.

~~~yaml
# Real extract from ''project.yaml'' file
# in its August 21, 2026 version.

###
# This key allows to specify a version number that complies with
# cf::''Semantic Versioning ; https://semver.org/'', such as ''1.0.0'',
# ''0.0.0-beta.1'', and ''0.3.1-beta.1+build.5''.
###
version *: sem_version

###
# This block allows to provide hyperlinks via the following keys, all
# of which are optional.
#
#   1. ''home'' allows to specify the address of a website dedicated to
#      the project.
#
#   1. ''dev'' is used to point to a repository for managing project
#      development.
#
#   1. ''issues'' redirects users to the page where they can report bugs
#      or make suggestions.
#
#
# note::
#     URLs are never verified automatically, but they can be validated
#     on demand (technically, this requires an internet connection, so
#     it is not possible to validate a URL every time an ''about.yaml''
#     file is analyzed).*
#
#
# Here is a fictitious example.
#
# yaml::
#     urls:
#       home  : https://github.com/bc-tools/for-dev
#       dev   : https://github.com/bc-tools/for-dev/tree/main/aboutmeta
#       issues: https://github.com/bc-tools/for-dev/issues
###
urls *:
  home, dev, issues *: url
~~~


#### The special case of alternatives

Documentation of an alternative requires that the various competing keys be documented in sections indicated by magic titles of the form `[[key-name]]`, as in the following example.

~~~yaml
# Real extract from ''project.yaml'' file
# in its August 21, 2026 version.

###
# [[doctitle]]
# This key must be used for a document-type project. This is because
# such a project must have a title.
#
#
# [[codename]]
# This key allows you to specify the name of a code-type project if
# it differs from that of the project folder.
#
#
# note::
#     If neither the ''codename'' nor ''doctitle'' key is used, the
#     project will be considered to be of code type.
###
codename | doctitle *: str +
~~~
