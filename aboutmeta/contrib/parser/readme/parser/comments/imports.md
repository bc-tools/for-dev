#### IMPORTS section (mandatory)

This section imports the libraries needed for the parser to work. It's mandatory, because you need to use at least `from aboutmeta.data.errors import ParsingError`. You can refine the imports like this.

  1. Before the comments `# ~~ PARSER ~~ #` and `# ~~ MAPPER ~~ #`, the imports cover all the coded functions.

  1. The comment `# ~~ PARSER ~~ #` is used to indicate imports specific to the `parse` function.

  1. The comment `# ~~ MAPPER ~~ #` indicates imports specific to the `map_List` function.


> ***TIP.*** *If you are only coding the parser, the use of the comments `# ~~ PARSER ~~ #` and `# ~~ MAPPER ~~ #` is completely unnecessary.*
