#!/usr/bin/env python3

import re

def transform_structure(text: str) -> str:
    lines = text.splitlines()
    output = []

    # 1. Isoler le header initial S
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "###":
            # Si c'est le header S, on le conserve tel quel au début
            block = []
            while i < len(lines):
                block.append(lines[i])
                if lines[i].strip() == "###" and len(block) > 1:
                    i += 1
                    break
                i += 1
            if "# S" in "\n".join(block):
                output.extend(block)
                output.append("")
                break
        else:
            i += 1

    # 2. Parcourir le reste pour associer chaque bloc ### au champ suivant
    pending_comment = []

    while i < len(lines):
        line = lines[i]

        # Détection d'un bloc de commentaires ###
        if line.strip() == "###":
            comment_block = []
            comment_indent = len(line) - len(line.lstrip())
            while i < len(lines):
                comment_block.append(lines[i])
                if lines[i].strip() == "###" and len(comment_block) > 1:
                    i += 1
                    break
                i += 1
            pending_comment = (comment_indent, comment_block)
            continue

        # Traitement des lignes clés/valeurs YAML
        if ":" in line:
            indent_len = len(line) - len(line.lstrip())
            indent_str = " " * indent_len
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()

            if val:
                # Clé avec valeur (ex: a: val-a)
                output.append(f"{indent_str}{key}:")
                if pending_comment:
                    c_indent, c_lines = pending_comment
                    # Le commentaire s'aligne sous la clé (+2 espaces)
                    for cl in c_lines:
                        output.append(f"{indent_str}  {cl.strip()}")
                    pending_comment = None
                # La valeur s'aligne sous le commentaire (+2 espaces)
                output.append(f"{indent_str}  {val}\n")
            else:
                # Clé parent sans valeur immédiate (ex: c:)
                output.append(f"{indent_str}{key}:")
                if pending_comment:
                    for cl in pending_comment[1]:
                        output.append(f"{indent_str}  {cl.strip()}")
                    pending_comment = None
                output.append("")

        i += 1

    return "\n".join(output)

# --- Test ---
text_input = """###
# S
#
# S'
###


###
# A
###
a: val-a

###
# B
###
b: val-b


###
# C
###
c:
  x:
###
# CC
###
    cc: val-cc"""

print(transform_structure(text_input))
