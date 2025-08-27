#### Project identity.

The keys `project.acronym`, `project.codename`, `project.doctitle`, and `project.desc` are used to quickly identify a project.


> ***IMPORTANT.*** *The key `desc` is mandatory.*


> ***WARNING!*** *`codename` and  `doctitle` can never be used at the same time.*


Here is how these different keys are used.

  1. `desc` is used to quickly describe the project.

  1. `acronym` explains the origin of an acronym: for example, `"[@]bout [Desc]ription"` explains the choice for the project name `@Desc`.

  1. `codename` allows you to specify the name of a code-type project if it differs from that of the project folder.

  1. `doctitle` must be used for a document-type project. This is because such a project must have a title.


> ***NOTE.*** *The last two points show that `aboutmeta` will assume that it is working with a code-type project by default.*
