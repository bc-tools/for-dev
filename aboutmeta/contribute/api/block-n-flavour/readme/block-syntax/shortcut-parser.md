### Shortcut for the last parser used

There is a shortcut to avoid typing the same parser name multiple times in succession: simply use a period (`.`).
Note that in the example below, `person | list(.)` sets the `person` parser, which is reused inside `list(.)`. However, the default parser does not become `list(person)` (since `list(person)` is not a parser), meaning `author` and `contrib` continue to use the `person` parser.
Conversely, `codename | doctitle *: str` sets the `str` parser.


<!-- SHORCUT PARSER - SIMPLIFIED VERSION - START -->

~~~yaml
# Simplified version of the ''project.yaml'' file (2026-10-27).

codename | doctitle *: str
desc: .

author | authors *: person | list(.)
contrib | contribs *: . | list(.)
~~~

<!-- SHORCUT PARSER - SIMPLIFIED VERSION - END -->
