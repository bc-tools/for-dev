### From internal Python data to YAML one

Alongside the `parse` function, a `write` function must be implemented to convert internal `Python` data into a standardized format for the `YAML` file.
There is **only one valid signature**: `write(data: object) -> object`. Generic types are shown here for illustration, but you must specify concrete type hints as demonstrated in the following snippet.


<!-- PARSER - WRITE FUNCTION - START -->

~~~python
# Extract from ''ymdate.py'' file (2026-10-27).

def write(data: datetime.date) -> str:
    return data.strftime('%Y-%m-%d')
~~~

<!-- PARSER - WRITE FUNCTION - START -->


> ***WARNING.*** *The `write` function bypasses normalization to preserve the user's original `YAML` input (for instance, retaining special characters in URLs rather than `HTML`-encoding them, which improves readability).*
