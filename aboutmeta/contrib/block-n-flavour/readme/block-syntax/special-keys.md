### Special keys

A little DSL allows you to define some special features for keys. Here's what you can use.

  1. To indicate **an optional key**, simply add the `*` character after its name, as in `key-name*`.

  1. An **alternative choice of keys**, i.e. only one key from a set of keys is allowed, use the character `|` as in `key-1-not-2 | key-2-not-1`, and if the keys are optional, simply use `key-1-not-2 | key-2-not-1 *`. You can use as many characters `|` as you need. Then, for the associated value, you can also use a similiar list of parsers like in `key-1-not-2 | key-2-not-1 : parser_1 | parser_2`, or just a single common parser `key-1-not-2 | key-2-not-1 : same_parser`.


> ***NOTE.*** *If one of the key is a list of data, just use `list(parser_name)`.*


Here is almost real extract extract from of the `project` block (in its August 7, 2025 version).


~~~yaml
# Almost real uncommented extract from ''project.yaml'' file,
# version of August 7, 2025.

version*: sem_version
date*: date

acronym*: str
desc: str

codename | doctitle *: str

author | authors *: person | list(person)

urls*:
  home*  : url
  dev*   : url
  issues*: url

require*:
  - str
~~~
