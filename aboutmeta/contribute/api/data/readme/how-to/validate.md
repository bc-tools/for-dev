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
        data_pb = DataPB(self)

        self._validate_email(data_pb)
        self._validate_affiliation(data_pb)

        return data_pb

    def _validate_email(
        self,
        data_pb: DataPB
    ) -> None:
        if self.email is None:
            return data_pb

        email = self.email

        try:
            data_pb.what(
                desc  = "EMAIL"
                value = email
            )

            validate_email(email)

            data_pb.success()

        except Exception as e:
            data_pb.failure(
                desc = f"EXCEPTION:\n{e}"
            )

        return data_pb

    ...
```


The special zero-argument method `validate` is used to validate data. It must return the number of problem found, and each problem found should be indicated using a log communication: see the `url.URL` class for a concrete example of its use.


> ***IMPORTANT.*** *As not all validation processes are considered 100% reliable, the `validate` method is only useful for terminal or log sessions.*
