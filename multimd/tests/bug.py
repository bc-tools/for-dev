from markdownify import markdownify as md

print(
    md(
        '<h1>Multiline title is allowed!</br>Section 1.2</h1>',
    )
)
