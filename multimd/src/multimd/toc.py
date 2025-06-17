#!/usr/bin/env python3

###
# This module XXXX.
###

def addtoc():
    ...

from markdown_it import MarkdownIt

md = MarkdownIt()

with open("README.md", encoding="utf-8") as f:
    text = f.read()

tokens = md.parse(text)

result = []

for t in tokens:
    print(f"\n[[{t.type}-{t.info}-{t.tag}]]\n{t.content}")
    # print(t.__dir__())
    input()

    # # Ignorer blocs de code markdown ou HTML
    # if t.type in ("fence", "html_block") and "<pre><code" in t.content:
    #     i += 1
    #     continue

    # # Extraire paragraphes sans code inline
    # if t.type == "paragraph_open":
    #     inline = tokens[i + 1]
    #     if inline.type == "inline":
    #         # Ne garder que les fragments non code
    #         parts = [
    #             child.content for child in inline.children
    #             if child.type != "code_inline"
    #         ]
    #         if parts:
    #             result.append("".join(parts).strip())
    #     i += 3  # skip paragraph_open, inline, paragraph_close
    #     continue

    # i += 1
