Using directly the API - Only a resume
--------------------------------------

Let's modify a little our first code (the ellipsis indicate the lines unchanged).

''`python
from spkpb import *

speaker = Speaker(
    logfile    = Path('mylog.log'),
    termstyle  = GLOBAL_STYLE_COLOR,
    onlyresume = True
)

...
''`

The use of ''onlyresume = True'' asks to print only the summaries of problems (that is useful for short processes with no need to be verbose). The terminal and the log file will show the following same verbose resume.

''`
---------------
1 WARNING FOUND
---------------

    * one/strange/file.txt
        + Some strange behaviors.

-------------
1 ERROR FOUND
-------------

    * one/bad/file.txt
        + Bad things appear.
''`
