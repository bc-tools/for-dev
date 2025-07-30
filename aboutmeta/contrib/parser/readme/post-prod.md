How to add post-production tools?
---------------------------------

XXXX

indiquer que pour le moment on a juste map_list à implémnter (choix fait car permetetra , si besoin de proposer map_dict pour les dict)

### Basic use case

juste besoin du parser lui-mêem


### Specific use case

 si besoin d'importer un parser en cours de dev dans les contribs, on passe via quelque chose comme suit où sont utilisés les parser person et sem_version en cours de dev dans le dossier contrib

 ~~~python
# --------------------------------- #
# -- << DEV >> POST-PROD IMPORTS -- #
# --------------------------------- #

# Here we do very ugly things that will not be reproduced in
# the final source code. DON'T DO THAT AT HOME!

from pathlib import Path
import sys

if not str(Path(__file__).parent) in sys.path:
    sys.path.append( str(Path(__file__).parent.resolve()) )

import person, sem_version
~~~
