import textwrap

text = """Lorem ipsum dolor XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX sit amet, consectetur adipiscing elit. Proin Proin Proin Proin sodalesnullaettin-ciduntimperdiet."""

chi = 40
indent = '    '  # 4 espaces

wrapped = textwrap.fill(
    text,
    width=chi,
    initial_indent=indent,
    subsequent_indent=indent,
    break_long_words=False,   # ⛔ ne coupe pas les mots longs
    break_on_hyphens=False    # ⛔ ne coupe pas sur les tirets non plus
)

print(wrapped)
