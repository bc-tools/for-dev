### Structure

The structure of the specifications mimics those that the user will be able to use, with the exception of lists of parsed data, which require the use of a single element list. In concrete terms, here's how it looks with a simplified extract from of the `project` block.

<!-- Simplified version - START -->
~~~yaml
# Simplified version of the ''project.yaml'' file (2026-08-21).

version: sem_version
desc: str
urls:
  home: url
  dev: url
  issues: url
require:
  - str
~~~
<!-- Simplified version - END -->

This code allows to use data such as the following, where the version will be analyzed by the `sem_version` parser, and URLs by the `url` parser. The `desc` data and the ones of the `require` list are kept as string values unparsed.

~~~yaml
# Fake example with funny links.

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


> ***IMPORTANT.*** *Nothing prevents you from expecting a dictionary or a list of values as a data to parse. In this case, you will delegate the analysis of this 'complex' data to the parser.*
