The `Python` module `spkpb`
===========================


> **I beg your pardon for my english...**
>
> English is not my native language, so be nice if you notice misunderstandings, misspellings, or grammatical errors in my documents and codes.


About `spkpb`
-------------

This module proposes two classes and one function that simplify the writing of programs which have to be verbose about a process on files and directories, and that have to emit informations, warnings and errors.

  1. `Speaker`, the `spk` of `spkpb`, has methods tho print informations on a terminal and/or in a log file.

  1. `Problems`, the `pb` of `spkpb`, allows to indicate and store warnings, "criticals" and errors.

  1. The function `timestamp` adds time stamps in a log file without printing anything in the terminal.


The following tutorial will starts with the hard way to work with the `spkpb` tools and finishes with more programmer-friendly tools.


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


Using directly the API - Just one output
----------------------------------------

You can either use only a log file or the terminal by omitting either `termstyle` or `logfile` when instanciating the class `Speaker`.


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


A ready-to-use communicating class
----------------------------------

We have seen the hard use of the API of `spkpb`. Indeed you can heritate the class `BaseCom` to do things easily: see the following code and outputs.


### `Python` code

~~~python
from spkpb import *

project = BaseCom(
    Problems(
        Speaker(
            logfile   = Path('mylog.log'),
            termstyle = GLOBAL_STYLE_COLOR
        )
    )
)

project.timestamp(kind = 'start')

project.new_warning(
    what = Path('one/strange/file.txt'),
    info = "some strange behaviors."
)

print(f'>>>>>>>> sucess = {project.success}')

project.new_error(
    what = Path('one/bad/file.txt'),
    info = "bad things appear."
)

print(f'>>>>>>>> sucess = {project.success}')

project.recipe(
    NL,
    'One basic showcase.',
    FORTERM,
        {VAR_STEP_INFO: 'ONLY FOR THE TERMINAL OUPUT!',
         VAR_LEVEL    : 1},
    FORLOG,
        {VAR_STEP_INFO: 'ONLY IN THE LOG FILE!',
         VAR_LEVEL    : 1},
)

project.resume()

project.recipe(NL)
project.timestamp(kind = 'end')
~~~


### The terminal output

~~~
1) [ #1 ] WARNING: some strange behaviors.
>>>>>>>> sucess = True
2) [ #2 ] ERROR: bad things appear.
>>>>>>>> sucess = False

One basic showcase.
    * ONLY FOR THE TERMINAL OUPUT!

---------------
1 WARNING FOUND
---------------

Look at the log file or above for details.

    * one/strange/file.txt
        + 1 warning.
          See #.: [1].

-------------
1 ERROR FOUND
-------------

Look at the log file or above for details.

    * one/bad/file.txt
        + 1 error.
          See #.: [2].
~~~


### The content of the log file `mylog.log`

~~~
---------------------------------------
START TIME STAMP: 2021-08-10 (11:40:02)
---------------------------------------

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

-------------------------------------
END TIME STAMP: 2021-08-10 (11:40:02)
-------------------------------------
~~~


Reset the management of problems
--------------------------------

### What we want...

A communicating process can be restarted several times. This needs to reset every informations stored and displayed. To acheive that, the classes `BaseCom`, `Problems` and `Speaker` all have a method `reset`. The following weird example shows how this method works.

### `Python` code

~~~python
from spkpb import *

project = BaseCom(
    Problems(
        Speaker(
            logfile   = Path('mylog.log'),
            termstyle = GLOBAL_STYLE_COLOR
        )
    )
)

project.new_warning(
    what = Path('one/strange/file.txt'),
    info = "some strange behaviors."
)

project.reset()

project.new_error(
    what = Path('one/bad/file.txt'),
    info = "bad things appear."
)

project.resume()
~~~


### The terminal output

Everything is printed but the summary only keeps what is after the use of the method `reset`.

~~~
1) [ #1 ] WARNING: some strange behaviors.
1) [ #1 ] ERROR: bad things appear.

-------------
1 ERROR FOUND
-------------

Look at the log file or above for details.

    * one/bad/file.txt
        + 1 error.
          See #.: [1].
~~~

Who has chosen this stupid example? :-)


### The content of the log file `mylog.log`

Everything before the use of the method `reset` is lost for ever.

~~~
1) [ #1 ] ERROR: bad things appear.

-------------
1 ERROR FOUND
-------------

    * one/bad/file.txt
        + See [ #.1 ] : bad things appear.
~~~
