###
# This module standardises the \md code generated in order to avoid
# any "false positive" \chges from \git's perspective.
###


from pathlib import Path
import re

# No need to rebuild a wheel...
from markdown_it import MarkdownIt
from markdownify import (
    MarkdownConverter,
    markdownify,
)


# --------------- #
# -- CONSTANTS -- #
# --------------- #

_UGLY_TAG_TOC = "M+u-L+t-I+m-D=T-o+C"

TAG_TOC     = "::TOC::"
TAG_TMP_TOC = f"::{_UGLY_TAG_TOC}::"
PATTERN_TOC = re.compile(rf"::TOC(-(\d+))?::")

TAG_ANCHOR         = "MULTIMD-TOC-ANCHOR"
TAG_TMP_MD_ANCHOR  = f"::{TAG_ANCHOR}-{{}}::\n{{}}"
PATTERN_TMP_ANCHOR = re.compile(rf"::{TAG_ANCHOR}-\d+::\n")


# -------------------------------------- #
# -- CLASS FOR CUSTOMISING CONVERSION -- #
# -------------------------------------- #

###
# This class is used to perform certain actions during the translation
# of \html code to \md performed by \markdownify.
#
# warning::
#     We cannot type the code as this is not done in the ''markdownify''
#     \proj.
###
class StdConverter(MarkdownConverter):
###
# We initialise certain \attrs outside the ''MarkdownConverter'' parent
# class.
###
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.anchor_nb  = -1
        self.nb_tag_TOC = 0
        self.depth_TOC  = 100 # "Infinite" depth....
        self.titles     = []  # But `7` would be OK.

###
# When converting a text, we must identify the use of ''::TOC::'' or
# ''::TOC-<depth>::'' by a user wishing to add a \toc.
###
    def process_text(self, el, parent_tags = None):
        text = super().process_text(el, parent_tags)

# Do we have a placeholder for a \toc?
        matched_toc = re.match(
            PATTERN_TOC,
            text
        )

        if (
            not 'code' in parent_tags
            and
            not matched_toc is None
        ):
            self.nb_tag_TOC += 1

            if matched_toc.groups() != -1:
                self.depth_TOC = matched_toc.groups()[1]

                if self.depth_TOC is None:
                    self.depth_TOC = 100

                else:
                    self.depth_TOC = int(self.depth_TOC)

            text = TAG_TMP_TOC

        return text

###
# We need to manage the titles added to an eventual \toc.
###
    def _convert_hn(self, n, el, text, parent_tags = None):
        title = super()._convert_hn(n, el, text, parent_tags)

        if (
            "blockquote" in parent_tags
            or
            n == 1
        ):
            return title

        title = title.lstrip()

        self.anchor_nb += 1

        self.titles.append((text, n, self.anchor_nb))

        return TAG_TMP_MD_ANCHOR.format(self.anchor_nb, title)

###
# Here we're fixing a small bug in the management of online codes
# containing the symbol ''`''.
###
    def convert_code(self, el, text, parent_tags = None):
# We are in a block code.
        if el.parent.name == "pre":
            return text

# We are in an inline code.
        code = el.get_text()

        if "`" in code:
            code = f"`{code}`"

        return f"`{code}`"

###
# We prefer to use ''~~~'' to delimit blocks of code.
###
    def convert_pre(self, el, text, parent_tags = None):
        code_el = el.find("code")

        if code_el:
            lang_classes = code_el.get("class", [])
            lang         = ""

            for cls in lang_classes:
                if cls.startswith("language-"):
                    lang = cls.replace("language-", "")
                    break

            code = code_el.get_text()

        else:
            lang = ""
            code = el.get_text()

        return f"\n~~~{lang}\n{code.strip()}\n~~~\n"
