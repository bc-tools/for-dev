import re
from pathlib import Path
import yaml

# Expression régulière pour les lignes de version
LINE_PATTERN = re.compile(r"==\s*(\d{1,2})\s*\((\d+\.\d+\.\d+(?:-[\w.]+)?)\)\s*==")

# Mois français → chiffre
MOIS_MAP = {
    "janvier": "01", "février": "02", "mars": "03", "avril": "04",
    "mai": "05", "juin": "06", "juillet": "07", "août": "08",
    "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"
}

def parse_file(path: Path, year="2025"):
    mois_nom = path.stem.lower()
    mois_num = MOIS_MAP.get(mois_nom)
    if not mois_num:
        print(f"⚠️ Mois inconnu : {path.name}")
        return []

    results = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        print(f"❌ Erreur de lecture : {path} ({e})")
        return []

    for i, line in enumerate(lines, start=1):
        match = LINE_PATTERN.search(line)
        if match:
            jour, version = match.groups()
            jour = jour.zfill(2)
            date_str = f"{year}-{mois_num}-{jour}"
            results.append({
                "version": version,
                "date": date_str,
                "line": i
            })
    return results

def scan_versions(root_dir="."):
    versions = []
    for txt_file in Path(root_dir).rglob("*.txt"):
        versions.extend(parse_file(txt_file))
    return versions

if __name__ == "__main__":
    data = scan_versions(".")
    with open("versions.yaml", "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print("✅ Fichier versions.yaml généré.")
