`YAML` specifications
---------------------

In this section, we present all level `1` blocks. In the following fictive example, these blocks are named `block-1`, `block-2`, and `block-3`.

~~~yaml
block-1:
  sub-block:
    Some text
    on several lines...

block-2:
  - element 1
  - element 2

block-3:
  - key-1: val-1
  - key-2: val-2
  - key-3: val-3
~~~


Here are the **conventions used in our explanations**.

  1. The concept of attribute will refer to a block, a key, etc.

  1. A virtual pointed path like `block-3.key-1` refers to the key `key-1` of block `block-3`.

  1. Optional attributes will be indicated by their name followed by an asterisk `*`.

  1. Sometimes, an attribute can be used either in the singular or plural form, but not both at the same time. In this case, the name will end with `(s)`, as in `author(s)`.


> ***NOTE.*** *If you are unfamiliar with the general syntax of `YAML`, the [Wikipedia article YAML][1] is a good place to start.*


> ***IMPORTANT.*** *Technically, `YAML` files are read securely by treating all values as simple character strings.*


[1]: https://wikipedia.org/wiki/YAML
