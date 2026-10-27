### Magic comments

A new block definition must include a minimum amount of documentation (these texts will be used for CLI help messages and documentation).


#### General block description

The following dummy code demonstrates how to succinctly describe the purpose of a block using a magic comment at the very beginning of the `YAML` specification file.

~~~yaml
###
# This initial comment **must** describe the block from
# a technical perspective.
###

# Next comes the content of the file.
~~~


> ***IMPORTANT.*** *Magic comments start and end with `###`. Their content should be written as end-user documentation, rather than developer-facing notes.*


#### How blocks and keys work

Following the general description, documenting sub-blocks or keys is optional but strongly recommended. Documentation should be added as comments immediately preceding the relevant block or key. Below are a few extracts from the `project.yaml` file; note that in the `urls` block, the `home`, `dev`, and `issues` keys are intentionally left undocumented.


<!-- HELPERS - NO ALT - START -->

~~~yaml
# Real extract from ''project.yaml'' file (2026-10-15).

###
# This key is for specifying the semantic version number of the
# project. See cf::''Semantic Versioning ; https://semver.org/''
# to learn how this works.
###
version *: sem_version

###
# This block allows to provide hyperlinks via the following keys,
# all of which are optional.
#
#   1. ''home'' allows to specify the address of a website
#      dedicated to the project.
#
#   1. ''dev'' is used to point to a repository for managing
#      project development.
#
#   1. ''issues'' redirects users to the page where they can
#      report bugs or make suggestions.
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

<!-- HELPERS - NO ALT - END -->


> ***WARNING.*** *You do not need to specify expected data types, as they are automatically covered by each parser's description.*


#### Special case of alternatives

Documenting an alternative choice requires defining each competing key in a section marked by a magic title of the form `[[key-name]]`, as shown in the following example.


<!-- HELPERS - WITH SOME ALTS - START -->

~~~yaml
# Real extract from ''project.yaml'' file (2026-10-27).

###
# [[doctitle]]
# This key must be used for a document-type project, because such
# a project must have a title.
#
#s
# [[codename]]
# This key allows you to specify the name of a code-type project
# if it differs from that of the project folder.
#
#
# important::
#     If neither the ''codename'' nor ''doctitle'' key is used,
#     the project will be considered to be of code type.
###
codename | doctitle *: str +
~~~

<!-- HELPERS - WITH SOME ALTS - END -->
