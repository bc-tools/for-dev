### Validate a data value

Just like normalization, a data value can also be validated : this is the role of the no-argument method `validate` that must return the number of problem found. Each problem found should be indicated using a log communication: see the `url.URL` class for a concrete example of its use.
