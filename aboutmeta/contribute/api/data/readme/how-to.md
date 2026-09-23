How to propose a new data object?
---------------------------------

> ***IMPORTANT.*** *Before adding a new data type class, make sure that a ready-made solution does not already exist. For reference, the `date` and `sem_version` parsers implemented by `aboutmeta` use `datetime.date` and `semver.Version` respectively to store data. If no reliable and well-established solution is available, the new data type class must comply with the rules described in the following sections.*


> ***WARNING.*** *The purpose of a data type class is limited to storing data via attributes, optionally performing data normalization (e.g., standardizing a valid URL format) and data validation when needed (e.g., verifying if a physical address exists using a web service). Parsing user input is the responsibility of parsers, not data type classes.*
