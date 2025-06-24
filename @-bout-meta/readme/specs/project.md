### Block `project`

Let's start with a full description of a fictive project.

~~~yaml
project:
  acronym: "[@]bout [Desc]"
  usename: a_desc

  desc   : Let's explain what is the project ''@Desc''...
  authors:
    - Ada, Lovelace [ada.babbage.computer@paper.org]
      (Victorian Institute of Applied Mechanical Informatic)
    - Jean-Louis, Krivine [jl-krivine@compile.brain]
    - Torvalds
      (Department of Sacred Kernels, Infernal Ranting Graduate School of Helsinki)

  licences:
    code  : gnu 3
    manual: gnu 3

  urls:
    repo  : https://github.com/bc-tools/for-latex/tree/main/tutodoc
    issues: https://github.com/bc-tools/for-latex/issues

  langs:
    manual: fr

  require:
    - latex
~~~
