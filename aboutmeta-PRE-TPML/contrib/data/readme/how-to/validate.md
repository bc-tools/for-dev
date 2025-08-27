### Validate a data parsed

The special zero-argument method `validate` is used to validate a data. It must return the number of problem found, and each problem found should be indicated using a log communication: see the `url.URL` class for a concrete example of its use.


> ***IMPORTANT.*** *As not all validation processes are considered 100% reliable, the `validate` method is only useful for terminal sessions.*
