##### URLs

XXXXXX



Although URLs are stored verbatim, we would like to point out here that `aboutmeta.AMData` is capable of testing the validity of URLs in the sense that they are associated with a DNS catalogue. In other words, a URL pointing nowhere will cause an error.
As this operation involves a basic web query, the user must make an explicit request as in the following code, even if the method used is risk-free.

~~~python
from aboutmeta import AMData, Path

meta = AMData(Path("/full/path/to/about.yaml"))
meta.build()

meta.validate_urls("project.urls")
~~~
