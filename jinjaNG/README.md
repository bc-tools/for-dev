The `Python` module `jinjaNG`
=============================

> **I beg your pardon for my english...**
>
> English is not my native language, so be nice if you notice misunderstandings, misspellings, or grammatical errors in my documents and codes.

This document is a short tutorial showing the most useful features without being exhaustive.


About `jinjaNG`
---------------

This small project tries to ameliorate the workflow when working with the template engine [Jinja](https://palletsprojects.com/p/jinja/).

  1. Structured specifications for tags to be used in a template.

  1. Filler data in `JSON`, `YAML`, or `Python` files.

  1. Work with either files or strings.

  1. Use of pre and post-processing.


Working with files
------------------

### Our goal

Suppose we want to type the following `LaTeX` code. This corresponds to a file with extension `TEX`.

~~~latex
\documentclass{article}

\begin{document}

One example.

\begin{enumerate}
    \item Value nb. 1: "one".
    \item Value nb. 2: "two".
    \item Value nb. 3: "three".
    \item Value nb. 4: "four".
    \item Value nb. 5: "five".
\end{enumerate}

\end{document}
~~~

As you can see, most of the content follows a repetitive logic. So it may be a good idea to automate the typing. Here is where `jinjaNG` can help us.



### What we really type

The first thing we can do is to define the repetitive content. Let's use a `YAML` file (a `JSON` file can be used, but it's less fun to type). If we need to go further into the numbers in the `LaTeX` file, we just have to add new names to the list in the `YAML` file.

~~~yaml
txt_exa: example
values :
  - one
  - two
  - three
  - four
  - five
~~~


Next, let's type a minimalist `LaTeX` code using special instructions and tags. Explanations are given below.

~~~latex
\documentclass{article}
%: if False
\usepackage{jnglatex}
%: endif

\begin{document}

One \JNGVALOF{txt_exa}.

\begin{enumerate}
%: for oneval in values
    \item Value nb. \JNGVALOF{loop.index}: "\JNGVALOF{oneval}".
%: endfor
\end{enumerate}

\end{document}
~~~

This is how the previous template was typed.

  1. Let's start with the content after the `\begin{document}`. With `\JNGVALOF{txt_exa}`, we indicate to use the value associated with the `txt_exa` variable in the `YAML` data file. In our case, `\JNGVALOF{txt_exa}` corresponds to `example`.

  1. At the begining of the template, the lines between `%: if False` and `%: endif` will not be in the final output. Here we use `%: some Jinja instructions` with an always-false condition which causes the block to be ignored when making the final file. This allows the `jnglatex` package to be used only in the template file, but not in the final output. This package allows `jinjaNG` variables to be clearly highlighted after the `LaTeX` template is compiled: this small feature greatly simplifies template design.


>  For now, the `jngutils.sty` file must be in the same folder as the `LaTeX` template, or it must be installed by hand in your `LaTeX` distribution: you will find it in the `jngutils` folder.



### Building the output via a `Python` code

Using a `Python` file, it is easy to produce the desired output. Here are the instructions to use where we assume that the `cd` command has been used beforehand, so that running the `Python` scripts is done from the folder containing our `Python`, `YAML` and `LaTeX` files.

~~~python
from jinjang import *

mybuilder = JNGBuilder()

mybuilder.render(
    data     = "data.yaml",
    template = "template.tex",
    output   = "output.tex"
)
~~~

This code uses one useful default behaviour: `jinjaNG` associates automatically the `LaTeX` dialect, or flavour because the template has the extension `TEX`. The flavours available are given in the last section of this document.



### Building the output via command lines

The commands below have the same effect as the `Python` code in the previous section.

~~~
> cd path/to/the/good/folder
> jinjang data.yaml template.tex output.tex
File successfully built:
  + output.tex
~~~



### Building the data via a `Python` script

In our case, by knowing the existence of [cvnum](https://pypi.org/project/cvnum/), for example, we can be more efficient in constructing the data. Here is one possible `data.py` file where `JNGDATA` is a reserved name for the data that `jinjaNG` will use. We'll see next that producing the final output can no longer be done using the default behaviour of an instance of the `JNGBuilder` class.

~~~python
from cvnum.textify import *

nameof = IntName().nameof

JNGDATA = {
    'txt_exa': "example",
    'values' : [nameof(x) for x in range(1, 6)]
}
~~~


The `Python` code producing the final output becomes the following one, where `pydata = True` allows the class `JNGBuilder` to execute the `Python` file. **This choice can be dangerous with untrusted `Python` scripts!**

~~~python
from jinjang import *

mybuilder = JNGBuilder(pydata = True)

mybuilder.render(
    data     = "data.py",
    template = "template.tex",
    output   = "output.tex"
)
~~~


To work with a `Python` data file from the terminal, you must use the tag `--unsafe` because **it can be dangerous to launch a `Python` data file**, so `jinjaNG` must know that you really want to do this. The commands below have the same effect as the `Python` code above.

~~~
> cd path/to/the/good/folder
> jinjang --unsafe data.py template.tex output.tex
WARNING: Using a Python file can be dangerous.
File successfully built:
  + output.tex
~~~


> Scripts like `data.py` can do relative imports.


Hooks: doing pre and post-processing
------------------------------------

### What we need?

In the previous section, we saw how to produce a `LaTeX` file by feeding a template. It would be handy to be able to compile the resulting file in `PDF` format to make it readable by anyone. To do this easily, `jinjaNG` offers the possibility to work with pre and post-processing, or "hooks".



### How to do this?

We need to work with a `YAML` configuration file. For simplicity, we use the default settings by working in a directory that looks like this.

~~~
+ myfolder
    * cfg.jng.yaml
    * data.json
    * template.tex
~~~


Writing external commands is done in the `cfg.jng.yaml` file. Here, we just use the `post` block for post-processing, but we could also use a `pre` block for pre-processing. Note the use of `{output}` which will be replaced by the path of the file built by `jinjaNG`.

~~~yaml
hooks:
  post:
    - latexmk -interaction=nonstopmode -pdf "{output}"
    - latexmk -interaction=nonstopmode -c   "{output}"
~~~

> One important thing to know is that the commands must be written relative to the parent folder of the template.


Once the `cfg.jng.yaml` file has been built, it is sufficient to do the following on the command line (we have omitted the output). The `auto` value of the `--config` option indicates that the configurations are in the `cfg.jng.yaml` file.

~~~
> cd path/to/the/myfolder
> jinjang --config auto data.json template.tex output.tex
[...]
~~~


The contents of `myfolder` have been changed as follows.

~~~
+ myfolder
    * cfg.jng.yaml
    * data.json
    * output.pdf
    * output.tex
    * template.tex
~~~


> If there are multiple templates in a folder, or to use test configurations, it is useful to be able to choose the configuration file explicitly.
> In this type of situation, it is sufficient to proceed via `jinjang --config path/to/speconfig.yaml ...` for example.


Working with `Python` variables
-------------------------------

To work directly from `Python` without using any file, you need to produce a dictionary for the data, and a string for the template, so as to get a string for the final output. Let's take an example where the dialect, or flavour, must be specified always.

~~~python
from jinjang import *

mydata = {
    'txt_exa': "small example",
    'max_i'  : 4
}

mytemplate = """
One {{ txt_exa }} with automatic calculations.
##: for i in range(1, max_i + 1) :##
  {{ i }}) I count using squares: {{ i**2 }}.
##: endfor :##
""".strip()

mybuilder = JNGBuilder(flavour = FLAVOUR_ASCII)

output = mybuilder.render_frompy(
    data     = mydata,
    template = mytemplate
)
~~~


The content of the string `output` will be the following one.

~~~markdown
One small example with automatic calculations.

  1) I count using squares: 1.

  2) I count using squares: 4.

  3) I count using squares: 9.

  4) I count using squares: 16.

~~~


All the flavours
----------------

To indicate a dialect for templates, a flavour must be given. Here are the minimalist technical descriptions of each of these flavours.


<!-- FLAVOURS - TECH. DESC. - START -->

---

#### Flavour `ascii`

> ***Short description:*** *generic behaviour of `jinjaNG`.*

  1. **Extensions for the auto-detection.**
      * Any extension not associated with another flavour is associated with that flavour (which is like a default one).

  1. **Tools to assist in typing templates.**
      * Nothing available.

  1. **Variables, `jinja` instructions and comments.**
  Here is a fictive `how-to` code.

~~~markdown
In our templates, we use {{variable}} .

It is always possible to work with block jinja instructions,
and comments.

##_ Comments: one basic loop. _##

##: for i in range(5) :##
We can use {{i + 4}} .
##: endfor :##

Most of flavours propose inline jinja instructions,
and comments.

#_ Comments: the same loop as above.

#: for i in range(5)
We can use {{i + 4}} .
#: endfor
~~~

---

#### Flavour `html`

> ***Short description:*** *useful settings and tools for HTML templating.*

  1. **Extension for the auto-detection.**
      * `HTML`

  1. **Tools to assist in typing templates.**
      * See the folder `jngutils/html`.

  1. **Variables, `jinja` instructions and comments.**
  Here is a fictive `how-to` code.

~~~markdown
In our templates, we use {{variable}} .

It is always possible to work with block jinja instructions,
and comments.

<!--_ Comments: one basic loop. _-->

<!--: for i in range(5) :-->
We can use {{i + 4}} .
<!--: endfor :-->

This flavour doesn't propose neither inline jinja instructions,
nor inline comments.
~~~

---

#### Flavour `latex`

> ***Short description:*** *useful settings and tools for LaTeX templating.*

  1. **Extensions for the auto-detection.**
      * `STY`
      * `TEX`
      * `TKZ`

  1. **Tools to assist in typing templates.**
      * See the folder `jngutils/latex`.

  1. **Variables, `jinja` instructions and comments.**
  Here is a fictive `how-to` code.

~~~tex
In our templates, we use \JNGVALOF{variable} .

It is always possible to work with block jinja instructions,
and comments.

%%_ Comments: one basic loop. _%%

%%: for i in range(5) :%%
We can use \JNGVALOF{i + 4} .
%%: endfor :%%

Most of flavours propose inline jinja instructions,
and comments.

%_ Comments: the same loop as above.

%: for i in range(5)
We can use \JNGVALOF{i + 4} .
%: endfor
~~~

---

#### Flavour `md`

> ***Short description:*** *useful settings for Markdown templating.*

  1. **Extension for the auto-detection.**
      * `MD`

  1. **Tools to assist in typing templates.**
      * Nothing available.

  1. **Variables, `jinja` instructions and comments.**
  Here is a fictive `how-to` code.

~~~md
In our templates, we use {{variable}} .

It is always possible to work with block jinja instructions,
and comments.

<!--_ Comments: one basic loop. _-->

<!--: for i in range(5) :-->
We can use {{i + 4}} .
<!--: endfor :-->

This flavour doesn't propose neither inline jinja instructions,
nor inline comments.
~~~

<!-- FLAVOURS - TECH. DESC. - END -->