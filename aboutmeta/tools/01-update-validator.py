from cerberus import Validator

class CustomValidator(Validator):
    def _validate_zero_or_one_of(self, constraint, field, value):
        """
        Custom rule: at most one of the given fields may be present.
        Usage: any field can declare 'zero_or_one_of': ['field1', 'field2']
        """
        if not isinstance(constraint, list):
            self._error(field, "zero_or_one_of must be a list")
            return

        count = sum(
            1 for key in constraint
            if key in self.document and self.document[key] not in (None, '', [], {}, False)
        )
        if count > 1:
            self._error(field, f"Only one of {constraint} is allowed (found {count})")

# Le schéma
schema = {
    'author': {'type': 'string', 'zero_or_one_of': ['author', 'authors']},
    'authors': {'type': 'list', 'schema': {'type': 'string'}, 'zero_or_one_of': ['author', 'authors']}
}

# Données à valider
docs = [
    {},  # ✅
    {'author': 'Alice'},  # ✅
    {'authors': ['Bob', 'Carol']},  # ✅
    {'author': 'Alice', 'authors': ['Bob']},  # ❌
]

# Test
v = CustomValidator(schema)

for i, doc in enumerate(docs, 1):
    print(f"\n🔍 Document {i}")
    if v.validate(doc):
        print("✅ Valid")
    else:
        print("❌ Invalid:", v.errors)
