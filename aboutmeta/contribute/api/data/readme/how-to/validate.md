### Validate data

The special zero-argument `validate` method is for data validation. It must use the `data_pb` attribute, as shown in the following partial example. Notice the use of the conveniently named methods `what`, `msg`, `success`, `failure`, and `exception`.

```python
# Extract of URL class code.
# Version 2026-09-26

import requests

from aboutmeta.core.data_manager import DataManager

...

class URL(DataManager):
    ...

    def validate(self) -> None:
        self._errors_found = []

        self._validate_DNS()
        self._validate_HTTP()

    def _validate_DNS(self) -> None:
        ...

    def _validate_HTTP(self) -> None:
        self.data_pb.what("HTTP status")

        url = self.url

        try:
            self.data_pb.info(f"Checking '{url}'")

            response = requests.head(
                url,
                timeout         = 3,
                allow_redirects = True
            )

            if response.status_code < 400:
                self.data_pb.info("OK: HTTP status validated.")

                return

            else:
                msg = f"'{url}': Requests status code = {response.status_code}."

                self.data_pb.error(msg)
                self._errors_found.append(msg)

        except Exception as e:
            msg = f"'{url}': {e}"

            self.data_pb.exception(msg)
            self._errors_found.append(msg)

        self.data_pb.info("KO: HTTP status unvalid.")

    ...
```


> ***IMPORTANT.*** *Since validation processes are not always 100% reliable, the `validate` method is primarily intended for terminal or logging sessions.*
