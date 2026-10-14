### From internal Python data to YAML one

Alongside the `parse` function, a `write` function must be coded to convert the internal `Python` data into a standardized string version for the `YAML` file. There is **only one possible signature** which is `write(data: object) -> str` (here, we use generic types for the `data` class, but you will have to be more precise, as in the accepted parsers).


> ***WARNING.*** *The `write` function bypasses normalization to preserve user-provided `YAML` input (e.g., keeping special characters in URLs instead of `HTML`-encoding them for readability).*
