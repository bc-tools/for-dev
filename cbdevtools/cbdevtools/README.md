The `Python` module `cbdevtools`
================================


> **I beg your pardon for my english...**
>
> English is not my native language, so be nice if you notice misunderstandings, misspellings, or grammatical errors in my documents and codes.


Last version: 0.0.11-beta
-------------------------

This version **0.0.11-beta** was made on **2022-08-11** .


About `cbdevtools`
-----------------

This project is a *"Common Box of Dev Tools"* (the name comes also from "Christophe BAL Dev Tools"). `cbdevtools` proposes small scripts that can be helpful... at least for the author of this package. :-)


### Append one package to `sys.path`

The function `addfindsrc.addfindsrc` adds one project folder to the system path.


Let's see one fictive example with the following tree structure.

~~~
+ mymod
    + doc
    + dist
    + src
        * __init__.py
        * ...
    + tools
        + debug
            * cli.py
~~~

The `Python` script `tools/debug/cli.py` can easily load the local
`Python` module `src` thanks to the module `addfindsrc` as it is shwon in the following code.

~~~python
from cbdevtools.addfindsrc import addfindsrc

addfindsrc(
    file    = __file__,
    project = 'mymod',
)

from src import *
~~~

If you need to have the path of the project added, just use the value returned by `addfindsrc.addfindsrc`.


***WARNING!*** *The directory of the project to add must contain the file `__file__`.*


### Selective version of the standard `dir(obj)`

Building automatically some `Python` scripts needs sometimes to play with `dir(obj)` of some classes, methods and functions. The function `shortdir.shortdir` can be helpful in this kind of situation.

Lets' consider the following code where the use of regexes allows enough flexibility to ignore some names.

~~~python
from pprint              import pprint
from cbdevtools.shortdir import (
    shortdir,
    re_compile, # Just an alias for ''re.compile''.
    PATTERN_UNDERSCORE # Pattern matching ''-...''.
)

print("shortdir(1) =")
pprint(shortdir(1))
print()

for toignore in [
    [],
    ['imag', 'real'],
    ['as_.+', 'from_.+']
]:
    toignore = [re_compile(s) for s in toignore]

    # For none empty list, we want also to ignore
    # the dunder methods.
    if toignore:
        toignore.append(PATTERN_UNDERSCORE)

    print(f"{toignore = }")

    print("shortdir(1, toignore) =")
    pprint(shortdir(1, toignore))
    print()
~~~

Launched in a terminal, this code produces the following output (the printings have been formatted, and truncated a little by hand to ease the reading).

~~~python
shortdir(1) = # Dunder methods ignored by default.
['as_integer_ratio',
 'bit_length',
 'conjugate',
 'denominator',
 'from_bytes',
 'imag',
 'numerator',
 'real',
 'to_bytes']

toignore = [] # To keep all the dunder methods.
shortdir(1, toignore) =
['__abs__',
 '__add__',
 '__and__',
 ..., #  Some other dunder methods.
 'as_integer_ratio',
 'bit_length',
 'conjugate',
 'denominator',
 'from_bytes',
 'imag',
 'numerator',
 'real',
 'to_bytes']

toignore = [
    re.compile('imag'),
    re.compile('real'),
    re.compile('_.*')
]
shortdir(1, toignore) =
['as_integer_ratio',
 'bit_length',
 'conjugate',
 'denominator',
 'from_bytes',
 'numerator',
 'to_bytes']

toignore = [
    re.compile('as_.+'),
    re.compile('from_.+'),
    re.compile('_.*')
]
shortdir(1, toignore) =
['bit_length',
 'conjugate',
 'denominator',
 'imag',
 'numerator',
 'real',
 'to_bytes']
~~~


### Signature of a callable object

To produce good quality code, it is very important to know the signature of a function, or a method. The purpose of the fucntion `.easysign`is to give an eays-to-use dictionary giving all the informations about a signature.

Let's start with the code above where we use `pprint` to obtain well formatted output.

~~~python
from pprint              import pprint
from cbdevtools.easysign import easysign

def funcOK(a:int, b: int = 1) -> str:
    ...

pprint(easysign(funcOK))
~~~

Launched in a terminal, we obtain the output below showing that the dictionary returned is very easy to use.

~~~
{'optional': ['b'],
 'params': {'a': {'default': None, 'typing': 'int'},
            'b': {'default': '1', 'typing': 'int'}},
 'return': 'str'}
~~~

***WARNING!*** *When nothing has been indicated in the original code, the value `None` is used.*


The signature of a method is also easy to obtain as it is done in the following code.

~~~python
class Test:
    def nothing(self):
        ...
    def noparam(self) -> str:
        ...
    def partialsign(self, a: str, b):
        ...
    def paramOK(self, a, b: bool = True) -> str:
        ...

mytest = Test()

for name in [
    "nothing",
    "noparam",
    "partialsign",
    "paramOK",
]:
    print(f"easysign(mytest.{name})")
    pprint(
        easysign(
            mytest.__getattribute__(name)
        )
    )
    print()
~~~

Here is the corresponding output.

~~~
easysign(mytest.nothing)
{'optional': [], 'params': {}, 'return': None}

easysign(mytest.noparam)
{'optional': [], 'params': {}, 'return': 'str'}

easysign(mytest.partialsign)
{'optional': [],
 'params': {'a': {'default': None, 'typing': 'str'},
            'b': {'default': None, 'typing': None}},
 'return': None}

easysign(mytest.paramOK)
{'optional': ['b'],
 'params': {'a': {'default': None, 'typing': None},
            'b': {'default': 'True', 'typing': 'bool'}},
 'return': 'str'}
~~~


To end this section, you have to know that using `easysign(1)` will raise the following error.

~~~
[...]
TypeError: 1 is not a callable object
~~~


### Using `orpyste` datas with `pytest`


The author of this package uses [orpyste](https://github.com/bc-python-OLD-IT-WILL-BE-REMOVED/orpyste) to work with ready-to-make `PEUF` data files in his tests.

To avoid problem with `pytest`, a fixture `peuf_fixture` is proposed wich follows the convention that the name of the `PEUF` file is obtained by removing the prefix `test_` from the name of the testing file Here is a real example of use with the following partial tree structure.

~~~
+ TeXitEasy
    + src
        * __init__.py
        * escape.py
    + tests
        + escape
            + fstringit.peuf
            + test_fstringit.py

~~~


The `Python` testing file `test_fstringit.py` is associated to the `PEUF` file `fstringit.peuf` where the prefix
`test_` has been removed. Using the datas stored in this `PEUF` file becomes very easy: here is the code used where
`tests` is an intuitive dictionary version of the `PEUF` file.

~~~python
from cbdevtools import *

addfindsrc(
    file    = __file__,
    project = 'TeXitEasy',
)

from src.escape import fstringit

def test_latex_use_fstringit(peuf_fixture):
    tests = peuf_fixture(__file__)

    for infos in tests.values():
        found  = fstringit(infos['source'])
        wanted = infos['fstring']

        assert wanted == found
~~~
