#!/usr/bin/env python3


# ------------- #
# -- PARSING -- #
# ------------- #

class ParsingError(Exception):
    ...

#     """
#     Exception levée lorsqu'une erreur de parsing se produit.

#     Attributes:
#         message (str): Message d'erreur expliquant la nature de l'erreur.
#         line_number (int, optional): Le numéro de ligne où l'erreur est survenue.
#         column_number (int, optional): Le numéro de colonne où l'erreur est survenue.
#          offending_text (str, optional): Le morceau de texte qui a causé l'erreur.
#     """
#     def __init__(self, message: str, line_number: int = None, column_number: int = None, offending_text: str = None):
#         super().__init__(message) # Appelle le constructeur de la classe parente (Exception)
#         self.message = message
#         self.line_number = line_number
#         self.column_number = column_number
#         self.offending_text = offending_text

#     def __str__(self):
#         """
#         Retourne une représentation en chaîne de caractères de l'exception,
#         plus détaillée si des informations de ligne/colonne sont disponibles.
#         """
#         if self.line_number is not None and self.column_number is not None:
#             return (f"ParsingError: {self.message} "
#                     f"at line {self.line_number}, column {self.column_number}."
#                     f"{f' Offending text: \'{self.offending_text}\'' if self.offending_text else ''}")
#         elif self.line_number is not None:
#             return (f"ParsingError: {self.message} "
#                     f"at line {self.line_number}."
#                     f"{f' Offending text: \'{self.offending_text}\'' if self.offending_text else ''}")
#         else:
#             return f"ParsingError: {self.message}"

# # --- Exemple d'utilisation ---

# def parse_data(data: str):
#     """
#     Simule une fonction de parsing qui peut lever une ParsingError.
#     """
#     lines = data.splitlines()
#     for i, line in enumerate(lines):
#         # Supposons qu'une ligne vide est une erreur de parsing dans ce contexte
#         # ou qu'une ligne spécifique est mal formatée
#         if not line.strip():
#             # Lever une ParsingError avec le numéro de ligne
#             raise ParsingError("Empty line found, cannot parse.", line_number=i+1)

#         if "ERROR_FORMAT" in line:
#             # Lever une ParsingError plus détaillée
#             col = line.find("ERROR_FORMAT") + 1
#             raise ParsingError(
#                 "Malformed data format detected.",
#                 line_number=i+1,
#                 column_number=col,
#                 offending_text=line[col-1:col+10] # Un extrait du texte problématique
#             )
#     return "Data parsed successfully!"

# # --- Tester l'exception ---

# print("--- Test 1: Ligne vide ---")
# try:
#     parse_data("Ligne valide 1\nLigne valide 2\n\nLigne valide 4")
# except ParsingError as e:
#     print(f"Exception capturée: {e}")
#     # Tu peux aussi accéder aux attributs spécifiques
#     print(f"  Message: {e.message}")
#     print(f"  Ligne: {e.line_number}")
#     print(f"  Colonne: {e.column_number}")
#     print(f"  Texte incriminé: {e.offending_text}")

# print("\n--- Test 2: Format incorrect ---")
# try:
#     parse_data("Donnée OK\nCeci contient une ERROR_FORMAT ici\nFin des données")
# except ParsingError as e:
#     print(f"Exception capturée: {e}")
#     print(f"  Message: {e.message}")
#     print(f"  Ligne: {e.line_number}")
#     print(f"  Colonne: {e.column_number}")
#     print(f"  Texte incriminé: {e.offending_text}")

# print("\n--- Test 3: Pas d'erreur ---")
# try:
#     result = parse_data("Donnée normale 1\nDonnée normale 2")
#     print(result)
# except ParsingError as e:
#     print(f"Cette exception ne devrait pas être levée ici: {e}")
