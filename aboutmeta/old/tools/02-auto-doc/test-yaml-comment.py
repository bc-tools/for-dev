import json
import re


def parse_dsl(texte):
    # 1. Normalisation totale des caractères invisibles
    texte = (
        texte.replace("\xa0", " ")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\u200b", "")
    )

    resultat = {}

    # 2. Extraire le premier gros bloc ### ... ### comme __main_comment__
    main_match = re.search(r"###\s*\n(.*?)\n\s*###", texte, re.DOTALL)
    if main_match:
        main_lines = [
            l.strip().lstrip("#").strip()
            for l in main_match.group(1).splitlines()
            if l.strip() and l.strip() != "#"
        ]
        resultat["__main_comment__"] = {
            "valeur": "",
            "commentaire": "\n".join(main_lines),
        }

    # 3. Regex pour capturer un commentaire ### # ... ### immédiatement suivi d'une ligne clé: valeur
    # Explication :
    # - ###\s*\n : ouverture du bloc
    # - ((?:[ \t]*#.*\n)+) : capture de TOUTES les lignes commençant par # (avec espaces optionnels)
    # - \s*###\s*\n : fermeture du bloc
    # - ([^\n#:]+:[^\n]+) : capture de la ligne "clé : valeur"
    pattern = re.compile(
        r"###\s*\n((?:[ \t]*#.*\n)+)\s*###\s*\n([^\n#:]+:[^\n]*)", re.MULTILINE
    )

    for match in pattern.finditer(texte):
        comment_block = match.group(1)
        key_val_line = match.group(2)

        # Nettoyage du commentaire
        comment_lines = []
        for line in comment_block.splitlines():
            clean = line.strip().lstrip("#").strip()
            if clean:
                comment_lines.append(clean)

        # Extraction clé / valeur
        if ":" in key_val_line:
            cle, valeur = key_val_line.split(":", 1)
            resultat[cle.strip()] = {
                "valeur": valeur.strip(),
                "commentaire": "\n".join(comment_lines),
            }

    return resultat




# Test
contenu = """###
# MAIN 1
#
# MAIN 2
#
# MAIN 3
###


###
# SUB 1_1
# SUB 1_2
###
contrib | contribs *:
###
# OK?
###
  subkey: . | list(.)


###
# SUB 2_1
# SUB 2_2
###
keywords *:
  - ."""

data = parse_dsl(contenu)
print(json.dumps(data, indent=2, ensure_ascii=False))
