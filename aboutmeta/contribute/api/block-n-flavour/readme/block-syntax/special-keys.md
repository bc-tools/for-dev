### Special keys

A small DSL allows you to define special features for keys. Here is what you can use.

  1. To indicate **an optional key**, simply add a space and a `*` character after its name, as in `key-name *`.

  1. For an **alternative choice of keys** (i.e., where only one key from a set is allowed), use the pipe character (`|`), as in `key-1-not-2 | key-2-not-1`. If these keys are optional, simply use `key-1-not-2 | key-2-not-1 *`.
  You can use as many `|` characters as needed.
  For the associated value, you can either provide a matching alternative of parsers, such as `key-1-not-2 | key-2-not-1 : parser_1 | parser_2`, or a single common parser, such as `key-1-not-2 | key-2-not-1 : same_parser`.

  1. Non-competing keys that share the same parser, whether optional or required, can be specified quickly by separating them with commas, avoiding repetitive declarations. For example, `key-1, key-2 * : same_parser` defines two optional keys that can be used together and rely on the same parser.


> ***NOTE.*** *When dealing with an alternative choice where one of the keys represents a list of data, simply use `list(parser_name)`.*


Here is a real extract from the `project` block, where all displayed keys are optional. Users can specify either `author` or `authors`. Within the `urls` sub-block, the `home`, `dev`, and `issues` keys are all available, but not mandatory.


<!-- SPECIAL KEYS - REAL EXTRACT (no '.' shortcut) - START -->

~~~yaml
# Simplified version of the ''project.yaml'' file (2026-08-21).

author | authors *: person | list(person)

urls *:
  home, dev, issues *: url

require *:
  - str
~~~

<!-- SPECIAL KEYS - REAL EXTRACT (no '.' shortcut) - END -->
