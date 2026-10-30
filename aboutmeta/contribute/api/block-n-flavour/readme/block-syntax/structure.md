### Structure

The structure of the specifications mirrors what users will need to use, with the exception of parsed data lists, which require a single-element list. In concrete terms, here is a simplified extract from the `project` block.


<!-- BLOCK STRUCTURE - SIMPLIFIED VERSION - START -->

~~~yaml
# Simplified version of ''project.yaml'' file (2026-08-21).

version: sem_version
desc: str
urls:
  home: url
  dev: url
  issues: url
require:
  - str
~~~

<!-- BLOCK STRUCTURE - SIMPLIFIED VERSION - END -->


This code enables the use of data such as the following, where the version is parsed by the `sem_version` parser and URLs by the `url` parser. The `desc` field and elements within the `require` list are kept as unparsed string values.


~~~yaml
# Dummy example with funny links.

version: 1.0.0
desc: Just a basic fake example.
urls:
  home  : https://xkcd.com/2973
  dev   : https://xkcd.com/1923
  issues: https://xkcd.com/1686
require:
  - python
  - yaml
~~~


> ***IMPORTANT.*** *Nothing prevents you from expecting a dictionary or a list of values as data to parse. In this case, you can delegate the parsing of this complex data to a parser. For example, the `toc_path` parser accepts either a string or a dictionary. See `contribute/api/data/code/toc_path.py`.*
