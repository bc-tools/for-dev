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
    re_compile('imag'),
    re_compile('real'),
    re_compile('_.*')
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
    re_compile('as_.+'),
    re_compile('from_.+'),
    re_compile('_.*')
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
