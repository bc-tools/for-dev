##### The project on the web

Although URLs are stored verbatim, we would like to point out here that `aboutmeta.Extract` is capable of testing the validity of URLs in the sense that they are associated with a DNS catalogue. In other words, a URL that points nowhere will cause an error.
As this operation involves a basic, risk-free web query, the user must make an explicit request as in the following code.

~~~python
from aboutmeta import Extract, Path

meta = Extract(Path("/full/path/to/about.yaml"))
meta.build()

meta.validate_urls("project.urls")
~~~
