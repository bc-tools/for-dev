YAML specifications for digital projects
----------------------------------------

In this section, we present level `1` blocks and keys useful for managing digital projects.


In the following fictive example, the level `1` blocks are named `block-1`, `block-2`, and `block-3`, and `main-key` is a level `1` key.

~~~yaml
main-key: Not only level 1 blocks!

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


Here are the **conventions that will be used in our explanations**.

  1. The concept of attribute will refer to a block, a key, etc.

  1. A virtual pointed path like `block-3.key-1` refers to the key `key-1` of the block `block-3`.


> ***NOTE.*** *If you are unfamiliar with the general syntax of `YAML`, the [Wikipedia article YAML][1] is a good place to start.*


---


> ***IMPORTANT.*** *Technically, `YAML` files are read securely by treating all values as simple character strings.*


[1]: https://wikipedia.org/wiki/YAML
