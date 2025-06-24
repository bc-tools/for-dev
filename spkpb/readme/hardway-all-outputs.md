Using directly the API - All the outputs
----------------------------------------

### `Python` code

Let's consider the following `Python` file where `Path` is the class proposed by the module `pathlib`. You have to know that the values of the arguments ''what'' are "stringified" (this allows to use either standard strings or advanced classes by defining your own ''__str__'' method for the resume output of problems, if you need it).

''`python
from spkpb import *

speaker = Speaker(
    logfile   = Path('mylog.log'),
    termstyle = GLOBAL_STYLE_COLOR
)

problems = Problems(speaker)

problems.new_warning(
    what = Path('one/strange/file.txt'),
    info = "some strange behaviors."
)

problems.new_error(
    what = Path('one/bad/file.txt'),
    info = "bad things appear."
)

speaker.recipe(
    NL,
    'One basic showcase.',
    FORTERM,
        {VAR_STEP_INFO: 'ONLY FOR THE TERMINAL OUPUT!',
         VAR_LEVEL    : 1},
    FORLOG,
        {VAR_STEP_INFO: 'ONLY IN THE LOG FILE!',
         VAR_LEVEL    : 1},
)

problems.resume()
''`

### The terminal output

Launching our `Python` code from a terminal, we will see the following output.

''`
1) [ #1 ] WARNING: some strange behaviors.
2) [ #2 ] ERROR: bad things appear.

One basic showcase.
    * ONLY FOR THE TERMINAL OUPUT!

---------------
1 WARNING FOUND
---------------

Look at the log file and/or above for details.

    * "one/strange/file.txt"
        + 1 warning.
          See #.: [1].

-------------
1 ERROR FOUND
-------------

Look at the log file and/or above for details.

    * "one/bad/file.txt"
        + 1 error.
          See #.: [2].
''`


### The content of the log file `mylog.log`

Launching our `Python` code, `mylog.log` will have the following content (just note that the resume is more verbose than the one in a terminal).


''`
1) [ #1 ] WARNING: some strange behaviors.
2) [ #2 ] ERROR: bad things appear.

One basic showcase.
    * ONLY IN THE LOG FILE!

---------------
1 WARNING FOUND
---------------

    * one/strange/file.txt
        + See [ #.1 ] : some strange behaviors.

-------------
1 ERROR FOUND
-------------

    * one/bad/file.txt
        + See [ #.2 ] : bad things appear.
''`
