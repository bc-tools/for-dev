Using directly the API - Time stamp in the log file
---------------------------------------------------

The following code shows how to use `timestamp` such as to add time stamps in the log file.

''`python
from spkpb import *

speaker = Speaker(
    logfile   = Path('mylog.log'),
    termstyle = GLOBAL_STYLE_COLOR
)

timestamp(
    speaker = speaker,
    kind    = 'start 1',
)

timestamp(
    speaker = speaker,
    kind    = 'start 2',
    with_NL = False,
)

timestamp(
    speaker = speaker,
    kind    = 'start 3',
)
''`

This will add the following lines in the log file `mylog.log` without printing anything in the terminal.

''`
-----------------------------------------
START 1 TIME STAMP: 2021-08-09 (00:40:02)
-----------------------------------------

-----------------------------------------
START 2 TIME STAMP: 2021-08-09 (00:40:02)
-----------------------------------------
-----------------------------------------
START 3 TIME STAMP: 2021-08-09 (00:40:02)
-----------------------------------------

''`
