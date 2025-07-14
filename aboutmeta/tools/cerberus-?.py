schema = {
    "project": {
        "type": "dict",
        "required": True,
        "schema": {
            "version": {"type": "string", "required": True},
            "acronym": {"type": "string", "required": True},
            "codename": {"type": "string", "required": True},
            "desc": {"type": "string", "required": False},
            "author": {"type": "string", "required": False},
            "urls": {
                "type": "dict",
                "required": True,
                "schema": {
                    "home": {"type": "string", "required": True},
                    "dev": {"type": "string", "required": True},
                    "issues": {"type": "string", "required": True},
                }
            },
            "licenses": {
                "type": "dict",
                "required": True,
                "schema": {
                    "code": {"type": "string", "required": True},
                    "manual": {"type": "string", "required": True},
                }
            },
            "langs": {
                "type": "dict",
                "required": True,
                "schema": {
                    "doc": {"type": "string", "required": True},
                    "manual": {"type": "string", "required": True},
                }
            },
            "require": {
                "type": "list",
                "schema": {"type": "string"},
                "required": True
            },
            "keywords": {
                "type": "list",
                "schema": {"type": "string"},
                "required": True
            },
        }
    }
}


def format_errors(errors, prefix=""):
    lines = []
    for field, issues in errors.items():
        path = f"{prefix}.{field}" if prefix else field
        if isinstance(issues, list):
            for item in issues:
                if isinstance(item, dict):
                    # Sous-dictionnaire d'erreurs
                    lines += format_errors(item, prefix=path)
                else:
                    lines.append(f"❌ {path} → {item}")
        elif isinstance(issues, dict):
            lines += format_errors(issues, prefix=path)
    return lines


from cerberus import Validator
import yaml

with open("test.yaml") as f:
    data = yaml.safe_load(f)

v = Validator(schema)

if v.validate(data):
    print("✅ YAML valide.")
else:
    print("❌ Erreurs de validation :")
    for line in format_errors(v.errors):
        print("  " + line)
