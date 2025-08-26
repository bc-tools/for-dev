#### Developers, authors and contributors

The keys `project.author`, which is mandatory, and `project.contrib`, which is optional, are used either in the singular form to indicate a single person, or in the plural form to indicate a list of people. Here is a fictitious use case.

~~~yaml
project:
  author: Ada, Lovelace

  contribs:
    - Alan, Turing
    - Donald, Knuth
~~~


The following forms of personal identification are managed.

  1. **Title (mandatory):** `Surname`, `First name, Compound surname`, `First name 1, First name 2, Long surname`... Hereinafter, we will refer to one of the above forms as `<title>`.

  1. **Email address (optional):** `<title> [one.id@provider.abc]` uses square brackets for the email.

  1. **Affiliation (optional):** `<title> (Name of institute, Country)` uses parentheses for the affiliation.

  1. **Indicate everything:** only the format `<title> [email] (institute)` is allowed.


> ***NOTE.*** *Emails are not verified, but they can be validated on demand (technically, this requires an internal connection, so it is not possible to validate an email every time an `about.yaml` file is analyzed).*
