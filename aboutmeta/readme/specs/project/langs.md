#### Languages

The optional `project.langs` block allows you to specify the languages used for the following cases related to a code-type project.

1. The `doc` key is for the language used to write the technical documentation.

1. The `manual` key is for the language used to write the user manual.


Language names must be those recognised by the `Python` package [`Babel`][1] used behind the scenes: see [ISO 639 standard][2] for languages and [ISO 3166 standard][3] for countries. For example, `fr_FR` indicates French spoken in France.


> ***NOTE.*** *The default language is `en_GB`.*


[1]: https://babel.pocoo.org/en/latest/
[2]: https://en.wikipedia.org/wiki/ISO_639
[3]: https://en.wikipedia.org/wiki/ISO_3166
