#!/usr/bin/env python3

import aboutmeta


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

from babel import localedata, Locale

lang_code = "en"

locale = Locale.parse(lang_code)
print("Nom en anglais :", locale.get_display_name('fr'))

# Cherche une locale complète qui commence par 'fr_'
default_locale = next(
    (loc for loc in localedata.locale_identifiers() if loc.startswith(lang_code + "_")),
    None
)

if default_locale:
    print(f"Locale par défaut trouvée pour '{lang_code}' : {default_locale}")
    default_territory = default_locale.split("_")[1]
    print(f"Territoire par défaut : {default_territory}")
else:
    print(f"Aucune locale étendue trouvée pour '{lang_code}'")

territories = sorted({
    loc.split("_")[1]
    for loc in localedata.locale_identifiers()
    if loc.startswith(f"{lang_code}_")
})

print(f"Territoires associés à '{lang_code}' :", territories)


from babel import Locale

# Obtenir le nom du territoire en français
locale_fr = Locale(lang_code)
print(f"{default_territory} → {locale_fr.territories['BE']}")  # France





# ----------------------------- #
# -- HUMAN TESTS (MANDATORY) -- #
# ----------------------------- #

if __name__ == "__main__":
    ...
