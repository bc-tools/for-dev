### Validate data






XXXX


gestion des pbs via la classe `DataPB` de méthodes...

    ... la data validée

    ... ce qui est validé

    ... Validtaion OK

    ... Validtaion KO avec dans ce cas un message (généralement l'excpetion levée)

    ... besoin de init dans cas cas pour initialiser data_pb au type de données, le reste étant utilisé par le validate


```python
# Extract of Person class code.
# Version 2026-09-26

from email_validator import validate_email

from aboutmeta.core.data_manager import (
    DataManager,
    DataPB
)

class Person(DataManager):
    ...

    def validate(self) -> DataPB:
        self._validate_email()
        self._validate_affiliation()

    def _validate_email(self) -> None:
        if self.email is None:
            return

        email = self.email

        try:
            self.data_pb.what("EMAIL")
            self.data_pb.msg(f"Checking {email}")

            validate_email(email)

            self.data_pb.success()

        except Exception as e:
            self.data_pb.exception(e)

    def _validate_affiliation(self) -> None:
        ...

    ...
```


The special zero-argument method `validate` is used to validate data. It must return the number of problem found, and each problem found should be indicated using a log communication: see the `url.URL` class for a concrete example of its use.


> ***IMPORTANT.*** *As not all validation processes are considered 100% reliable, the `validate` method is only useful for terminal or log sessions.*
