### Extraction des données

L'analyse d'un fichier `about.yaml` se fait simplemnt comme suit.

~~~python
from aboutmeta import AboutMeta, Path

meta = AboutMeta(Path("/full/path/to/about.yaml"))
meta.build()
~~~


> ***NOTE.*** *XXXXXXX*
