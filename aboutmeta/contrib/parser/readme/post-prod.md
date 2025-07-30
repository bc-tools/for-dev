How to add a post-production tool?
----------------------------------

Some flavors use lists of data of the same type that require modification as a whole once each piece of data has been parsed: for a real-world use case, see the description of the `map_list` function inside `contrib/parser/code/virtual_path.py`. Let's see how to do this at home.

> ***CAUTION!*** By choice, only "simple" data lists are currently allowed (end users cannot create dictionaries with their own keys).


### Only the parser for the list data is used

XXXX

juste besoin du parser lui-mêem





  1. ????
  Here are **the only possible signatures** for this function.

     + `map_list(data_list)` ????

     + `map_list(parent, data_list)` ????


### Other parsers are also involved

XXXX

 si besoin d'importer un parser en cours de dev dans les contribs, on passe via quelque chose comme suit où sont utilisés les parser person et sem_version en cours de dev dans le dossier contrib

 ~~~python
# --------------------------------- #
# -- << DEV >> POST-PROD IMPORTS -- #
# --------------------------------- #

# Ugly hacks just for the contribution phase.
#
# DON'T DO THAT AT HOME!

from pathlib import Path
import sys

if not str(Path(__file__).parent) in sys.path:
    sys.path.append(str(Path(__file__).parent.resolve()))

import person, sem_version
~~~
