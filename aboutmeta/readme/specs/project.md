### The project itself

Let's start with a complete description of a fictional code project.

~~~yaml
project:
  version*: 0.0.0-beta.1 (2025-06-27)

  acronym* : "[@]bout [Desc]"
  codename*: a_desc
  desc     : Let's explain what is the project ''@Desc''...

  author(s):
    - Ada, Lovelace [ada.babbage.computer@paper.org]
      (Victorian Institute of Applied Mechanical Informatic)
    - Jean, Louis, Krivine [jl-krivine@compile.brain]
    - Torvalds
      (Department of Sacred Kernels, Infernal Ranting Graduate School of Helsinki)

  urls*:
    home*  : https://github.com/bc-tools/for-latex
    issues*: https://github.com/bc-tools/for-latex/issues
    dev*   : https://github.com/bc-tools/for-latex/tree/main/tutodoc

  licences*:
    code*  : gnu 3
    manual*: cc by 4

  langs*:
    doc*   : fr
    manual*: fr

  require*:
    - python3
    - latex

  keywords*:
    - HHH
    - HHH
    - HHH
~~~


In the case of a document-type project, the `project.codename` key is no longer usable and must be replaced by `project.doctitle` (a document must have a title).


> ***NOTE.*** *By default, the project will be considered a code project.*


The following sections detail the use and meaning of the various attributes shown above.
