### Structure

The structure of the specifications mimics those that the user will be able to use, with the exception of lists, which require the use of a single element list. In concrete terms, here's how it looks with a simplified extract from of the `project` block.


~~~yaml
# Simplified version of the ''project.yaml'' file
# in its August 21, 2026 version.

version: sem_version
desc: str
urls:
  home: url
  dev: url
  issues: url
require:
  - str
~~~


This code allows to use data such as the following, where the version will be analyzed by the `sem_version` parser, and URLs by the `url` parser. The `desc` data and the ones of the `require` list are kept as string values.

~~~yaml
# Fake example.

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
