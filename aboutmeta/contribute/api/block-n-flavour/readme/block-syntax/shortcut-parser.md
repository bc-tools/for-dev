### Shortcut for the last parser used

There's a shortcut to avoid typing the same parser name several times in succession: just use a period. Bear in mind that in the actual extract below, the use of `person | list(.)` marks the `person` parser, which is reused in `list(.)`, but that the default parser does not become `list(person)`, which is not a parser, therefore `author` and `contrib` use the same `person` parser.


~~~yaml
# Simplified version of the ''project.yaml'' file
# in its August 21, 2026 version.

codename | doctitle *: str +
desc: .

author | authors *: person | list(.)
contrib | contribs *: . | list(.)
~~~
