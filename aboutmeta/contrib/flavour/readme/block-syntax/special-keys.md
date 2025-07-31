### Special keys

A little DSL allows you to define some special features for keys. Here's what you can use.

  1. An alternative choice of keys, that is the poissibility uses only one of a set of keys, use `|` like in `key-1-not-23 | key-2-not-13 | key-3-not-12`, and if these keys are optional, just use `key-1-not-23 | key-2-not-13 | key-3-not-12 *`.

  1. To indicate **an optional key**, simply add the `*` character after its name, as in `key-name *`.

  1. An **alternative choice of keys**, i.e. only one key from a set of keys is allowed, use `|` as in `key-1-not-2 | key-2-not-1`, and if the keys are optional, simply use `key-1-not-2 | key-2-not-1 *`. You can use as many `|` as you need. Then you have to use a similiar list of parsers like in `key-1-not-2 | key-2-not-1 : parser-1 | parser-2`.


> ***NOTE.*** *If one of the key is a list of data, just use `list(parser_name)`.*


Here is almost real extract extract from of the `project` block (in its July 31, 2025 version).


~~~yaml
# Almost real uncommented extract from ''project.yaml'' file,
# version of July 31, 2025.

version*: version
date*: date

acronym*: str
desc: str

author | authors *: person | list(person)

urls*:
  home*  : url
  dev*   : url
  issues*: url

require*:
  - str
~~~
