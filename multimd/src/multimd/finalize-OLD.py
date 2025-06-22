from collections.abc import Sequence
import inspect
from typing import Any, ClassVar, Protocol

from pathlib import Path
import re

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

MD_TAGS = list(FOCUS) + [
    'blockquote',
    'p',
]

TAG_TOC            = "::TOC::"
TAG_TMP_ANCHOR     = "MULTIMD-TOC-ANCHOR"
PATTERN_TMP_ANCHOR = re.compile(
    rf"::{TAG_TMP_ANCHOR}-(\d+)::\n"
)
TAG_TMP_MD_ANCHOR     = f"::{TAG_TMP_ANCHOR}-{{}}::\n"

###
# XXX
#
# refs::
#     - https://github.com/executablebooks/markdown-it-py/blob/master/markdown_it/renderer.py
###
class RendererStdMD(RendererHTML):
    __output__ = "standrard markdown"

###
# XXX
###
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.code_in_title   = False
        self.we_are_in_title = False
        self.title_deco_len  = 0
        self.title_content   = []
        self.titles          = []

        self.blockquote_content = []

        self.nb_tag_TOC   = 0
        self.metadata_TOC = []
        self.anchor_nb    = 0

###
# XXX
###
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

# Nothing to do.
        if token.hidden:
            return ""

# Ugly HTML code to keep
# ----------------------
#
# Keep HTML format when no equivalent markdown aletranative exists.
        tag = token.tag

        if (
            self.renderAttrs(token)
            or
            not tag in MD_TAGS
            and
            tag[0] != "h"
        ):
            return super().renderToken(
                tokens,
                idx,
                options,
                env,
            )

# Only MD syntax
# --------------
#
# Newline: see ''RendererHTML'' code.
#
# quote::
#     Insert a newline between hidden paragraph and subsequent opening
#     block-level tag.
#
#     For example, here we should insert a newline before blockquote:
#      - a
#        >
        if token.block and token.nesting != -1 and idx and tokens[idx - 1].hidden:
            result += "\n"

# Check if we need to add a newline after this tag
        if token.block:
            add_line_after = True

            if token.nesting == 1 and (idx + 1 < len(tokens)):
                nextToken = tokens[idx + 1]

                if nextToken.type == "inline" or nextToken.hidden:
# Block-level tag containing an inline tag.
                    add_line_after = False

                elif nextToken.nesting == -1 and nextToken.tag == token.tag:
# Opening tag + closing tag of the same type. E.g. `<li></li>`.
                    add_line_after = False

# A section title.
        if tag[0] == 'h':
            result += self.md_title(
                token,
                level = tag[1]
            )

# A blockquote.
        # elif tag == 'blockquote':
        #     self.we_are_in_blockquote = True# bool(token.nesting == -1)

# A focusing tag.
        elif tag in FOCUS:
            result += FOCUS[tag]

# A paragraph.
        elif tag == 'p':
            if add_line_after:
                result += "\n"*2

# Nothing left to do.
        return result

###
# XXX
###
#     def md_blockquote(
#         self,
#         token,
#     )
# self.blockquote_content

###
# XXX
###
    def md_title(
        self,
        token,
        level
    ):
        result = ""

        if token.nesting == -1:
            self.titles.append((
                "\n".join(self.title_content),
                int(level)
            ))

        else:
            result += TAG_TMP_MD_ANCHOR.format(self.anchor_nb)

            self.anchor_nb += 1

        if level in DECO_SECTION_12:
            if token.nesting == -1:
                result += "\n"
                result += DECO_SECTION_12[level]*self.title_deco_len
                result += "\n"*2

        elif token.nesting != -1:
            result += "#"*int(level)
            result += " "

        else:
            result += "\n"*2

        if token.nesting == -1:
            self.we_are_in_title       = False
            self.title_deco_len = 0
            self.title_content  = []

        else:
            self.we_are_in_title = True

        return result

###
# XXX
###
    def code_inline(
        self,
        tokens : Sequence[Token],
        idx    : int,
        options: OptionsDict,
        env    : EnvType
    ) -> str:
        content = tokens[idx].content

        if "`" in content:
            content = f"``{content}``"

        else:
            content = f"`{content}`"

        if self.we_are_in_title:
            self.code_in_title = True

            if self.title_content:
                self.title_content[-1] += content

            else:
                self.title_content = [content]

        else:
            self.code_in_title = False

        return content

###
# XXX
###
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

###
# XXX
###
    def text(
        self, tokens: Sequence[Token], idx: int, options: OptionsDict, env: EnvType
    ) -> str:
        content = tokens[idx].content

# We need to know the len of a title for the two first levels.
        if self.we_are_in_title:
            self.title_deco_len = max(
                self.title_deco_len,
                len(content)
            )


            if self.code_in_title:
                self.code_in_title = False

                if self.title_content:
                    self.title_content[-1] += content

                else:
                    self.title_content = [content]

            else:
                self.title_content.append(content)

        elif content == TAG_TOC:
            self.nb_tag_TOC += 1

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
# Can we erase an existing file?
    if not erase and dest.is_file():
        raise IOError(
            f"the function stdit is not allowed "
            "to erase the final file:"
            "\n"
            f"{dest}"
        )

# Markdown version keepin ''::TOC::''.
    mdit = MarkdownIt(
        renderer_cls   = RendererStdMD,
        options_update = {
            # 'breaks': True,
            'html'  : True
        }
    )

    md_std = mdit.render(
        src.read_text(encoding = "utf8")
    )
    md_std = md_std.rstrip() + "\n"

# Markdown version with ''::TOC::''?
    infos = mdit.renderer

# Misue of ''::TOC::''.
    if infos.nb_tag_TOC > 1:
        raise ValueError(
            f"Too many ''{TAG_TOC}'' used."
        )

# No ''::TOC::''.
    elif infos.nb_tag_TOC == 0:
        md_std = re.sub(
            PATTERN_TMP_ANCHOR,
            '',
            md_std,
        )

# Let's build the ToC.
    else:
        md_std = re.sub(
            PATTERN_TMP_ANCHOR,
            rf'<a id="{TAG_TMP_ANCHOR}-\1"></a>\n',
            md_std,
        )

        old_lines = md_std.split('\n')
        md_std    = []

        for line in old_lines:
            if line == TAG_TOC:
                toc_html = []

                for i, (title, level) in enumerate(infos.titles):
                    if level == 1:
                        continue

                    tab   = "  "*(level- 2)
                    title = title.replace("\n", "</br>")

                    toc_html.append(
                        f"{tab}- [{title}](#{TAG_TMP_ANCHOR}-{i})"
                    )

                line = "\n".join(toc_html)


            md_std.append(line)

        md_std = "\n".join(md_std)

# Nothing left to do.
    dest.touch()
    dest.write_text(
        data     = md_std,
        encoding = "utf8"
    )
