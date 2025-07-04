#### Developers, authors and contributors

The keys `project.author`, which is mandatory, and `project.contrib`, which is optional, are used either in the singular to indicate a single person, or in the plural to indicate a list of people. Here is a fictitious use case.

~~~yaml
project:
  author: Ada, Lovelace

  contribs:
    - Alan, Turing
    - Donald, Knuth
~~~


By default, the following forms of personal identification are available.

  1. **Title (mandatory):** `Surname`, `First name, Compound surname`, `First name 1, First name 2, Long surname`... Hereinafter, we will refer to one of the above forms as `<title>`.

  1. **Email address (optional):** `<title> [un.id@provider.abc]` (use of square brackets).

  1. **Institute or organisation (optional):** `<title> (Name of institute)` (use of parentheses).

  1. **Indicate everything:** the formats `<title> [email] (institute)` and `<title> (institute) [email]` are both allowed.
