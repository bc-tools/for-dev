### Shortcut for the last parser used

There's a shortcut to avoid typing the same parser name several times in succession: just use a period. Bear in mind that in the actual extract below, the use of `person | list(.)` marks the `person` parser, which is reused in `list(.)`, but that the default parser remains `person`, and does not become `list(person)`, which is not a parser, donc `author` and `contrib` use the same parser.


~~~yaml
# Uncommented real extract from ''project.yaml'' file,
# version of July 31, 2025.

version*: version
date*: date

acronym*: str
desc: .

author | authors *: person | list(.)
contrib | contribs *: . | list(.)

urls*:
  home*  : url
  dev*   : .
  issues*: .

require*:
  - str
~~~
