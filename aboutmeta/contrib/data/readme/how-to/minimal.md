### Minimum requirements

At the very least, your class must be structured as follows.

~~~python
from dataclasses  import dataclass

from aboutmeta.core.dataprinter import *

@dataclass(frozen = True)
class MyDataClass(DataPrinter):
    std : str
~~~


XXXX

Ceci est imposé pour les raisons suivantes.

    1)

    --> obligation de rensigner tous les attributs

    --> avec std attribut commun, on peut utiliser interface core.dataprinter

    --> possibilité d'enrichier le comportement de certains types de données : cf license.License, et pou autre éthode ok sauf validate et normalize qui sont bloqués
