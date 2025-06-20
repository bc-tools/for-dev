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


DECO_SECTION_12 = {
    '1': "=",
    '2': "-",
}

FOCUS = {
    'em'    : "*",
    'strong': "**",
}

# Source
#     - https://github.com/executablebooks/markdown-it-py/blob/master/markdown_it/renderer.py

class RendererStdMD(RendererHTML):
    __output__ = "standrard markdown"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.in_title          = False
        self.title_deco_len    = 0
        self.line_before_title = False


    def renderToken(
        self,
        tokens : Sequence[Token],
        idx    : int,
        options: OptionsDict,
        env    : EnvType,
    ) -> str:
        token = tokens[idx]

        add_line_after = False
        result         = ""


        # Tight list paragraphs
        if token.hidden:
            return ""

        # Insert a newline between hidden paragraph and subsequent opening
        # block-level tag.
        #
        # For example, here we should insert a newline before blockquote:
        #  - a
        #    >
        #
        if token.block and token.nesting != -1 and idx and tokens[idx - 1].hidden:
            result += "\n"

        # Check if we need to add a newline after this tag
        if token.block:
            add_line_after = True

            if token.nesting == 1 and (idx + 1 < len(tokens)):
                nextToken = tokens[idx + 1]

                if nextToken.type == "inline" or nextToken.hidden:
                    # Block-level tag containing an inline tag.
                    #
                    add_line_after = False

                elif nextToken.nesting == -1 and nextToken.tag == token.tag:
                    # Opening tag + closing tag of the same type. E.g. `<li></li>`.
                    #
                    add_line_after = False

        tag = token.tag

        if tag == 'p':
            if add_line_after:
                result += "\n"*2


        elif tag[0] == 'h':
            level = tag[1]

            if level in DECO_SECTION_12:
                if token.nesting == -1:
                    result += "\n"
                    result += DECO_SECTION_12[level]*self.title_deco_len
                    result += "\n"*2

                    self.in_title       = False
                    self.title_deco_len = 0



                else:
                    self.in_title       = True
                    self.title_deco_len = 0


            elif token.nesting != -1:
                result = "#"*int(level)
                result += " "

            else:
                result += "\n"*2

        elif tag in FOCUS:
            result += FOCUS[tag]


        else:
            # Add token name, e.g. `<img`
            result += ("</" if token.nesting == -1 else "<") + token.tag

            # Encode attributes, e.g. `<img src="foo"`
            result += self.renderAttrs(token)

            # Add a slash for self-closing tags, e.g. `<img src="foo" /`
            if token.nesting == 0 and options["xhtmlOut"]:
                result += " /"

            result += ">\n" if add_line_after else ">"

        return result


    def code_inline(
        self,
        tokens : Sequence[Token],
        idx    : int,
        options: OptionsDict,
        env    : EnvType
    ) -> str:
        token = tokens[idx]
        return  f"`{tokens[idx].content}`"

    def fence(
        self,
        tokens : Sequence[Token],
        idx    : int,
        options: OptionsDict,
        env    : EnvType,
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

    def text(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        content = tokens[idx].content

        if self.in_title:
            self.title_deco_len = max(
                len(content),
                self.title_deco_len
            )

        return content

###
# prototype::
#     src   : the path of the MD file to standardise.
#     dest  : the path of the standardised final path::''MD'' file to build.
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
