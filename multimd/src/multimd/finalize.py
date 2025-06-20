from collections.abc import Sequence
import inspect
from typing import Any, ClassVar, Protocol

from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.renderer import (
    RendererHTML,
    Token,
    EnvType, OptionsDict
)

# Source
#     - https://github.com/executablebooks/markdown-it-py/blob/master/markdown_it/renderer.py

class RendererStdMD(RendererHTML):
    __output__ = "standrard markdown"


    @staticmethod
    def renderAttrs(token: Token) -> str:
        result = ""

        for key, value in token.attrItems():
            result += " " + key + '="' + (str(value)) + '"'

        return result

    def renderInlineAsText(
        self,
        tokens: Sequence[Token] | None,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        result = ""

        for token in tokens or []:
            if token.type == "text":
                result += token.content
            elif token.type == "image":
                if token.children:
                    result += self.renderInlineAsText(token.children, options, env)
            elif token.type == "softbreak":
                result += "\n"

        return result


    def code_inline(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        token = tokens[idx]
        return  f"`{tokens[idx].content}`"

    def code_block(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        token = tokens[idx]

        return (
            "<pre"
            + self.renderAttrs(token)
            + "><code>"
            + escapeHtml(tokens[idx].content)
            + "</code></pre>\n"
        )

    def fence(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        token = tokens[idx]
        info = (token.info).strip() if token.info else ""
        langName = ""
        langAttrs = ""

        if info:
            arr = info.split(maxsplit=1)
            langName = arr[0]
            if len(arr) == 2:
                langAttrs = arr[1]

        if options.highlight:
            highlighted = options.highlight(
                token.content, langName, langAttrs
            ) or (token.content)
        else:
            highlighted = (token.content)

        if highlighted.startswith("<pre"):
            return highlighted + "\n"

        return f"""
~~~{langName}
{highlighted}~~~
        """.strip() + "\n"*2


    def image(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        token = tokens[idx]

        # "alt" attr MUST be set, even if empty. Because it's mandatory and
        # should be placed on proper position for tests.
        if token.children:
            token.attrSet("alt", self.renderInlineAsText(token.children, options, env))
        else:
            token.attrSet("alt", "")

        return self.renderToken(tokens, idx, options, env)

    def hardbreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        return "<br />\n" if options.xhtmlOut else "<br>\n"

    def softbreak(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        return (
            ("<br />\n" if options.xhtmlOut else "<br>\n") if options.breaks else "\n"
        )

    def text(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        return tokens[idx].content

    def html_block(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        return tokens[idx].content

    def html_inline(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        return tokens[idx].content














###
# prototype::
#     src   : the path of the MD file to standardise.
#     dest  : the path of the single final path::''MD'' file to build.
#     erase : set to ''True'', this argument allows to erase an existing
#             final file to build a new one.
###
def stdit(
    src  : Path,
    dest : Path,
    erase: bool = False
) -> None:
    if not erase and dest.is_file():
        raise IOError(
            f"the function stdit is not allowed "
            "to erase the final file:"
            "\n"
            f"{dest}"
        )

    mdit = MarkdownIt(
        renderer_cls   = RendererStdMD,
        options_update = {
            'breaks': True,
            'html'  : True
        }
    )

    md_std = mdit.render(src.read_text())

    dest.touch()
    dest.write_text(md_std)
