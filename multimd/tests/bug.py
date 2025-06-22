from markdownify import MarkdownConverter

class CustomMarkdownConverter(MarkdownConverter):
    def convert_hN(self, n, el, text, parent_tags):
        title = super().convert_hN(n, el, "text", parent_tags)

        return f"BUG: {title}"

def custom_markdownify(html):
    return CustomMarkdownConverter().convert(html)

# Exemple HTML
html = """
<h1>Section 1</h1>
<h2>Section 2</h2>
<h3>Sub Section 3.1</h3>
"""

print(custom_markdownify(html))
