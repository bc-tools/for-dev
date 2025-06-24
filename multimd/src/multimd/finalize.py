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


# ------------------------------ #
# -- THE CUSTOMISATION ITSELF -- #
# ------------------------------ #

###
# prototype::
#     :return: a replacement \func to number the \tmp anchors for an
#              eventual \toc.
#
# note::
#     We use a closure to define a \func to replace groups captured by
#     the ''PATTERN_TMP_ANCHOR'' regex pattern.
#     This \tech allows to number the \tmp anchors for an eventual \toc
#     by using a ''nonlocal'' \var.
###
def update_anchor_HTML():
    anchor_nb_HTML = -1

###
# prototype::
#     match : a group captured by the ''PATTERN_TMP_ANCHOR'' regex
#             pattern.
#
#     :return: the replacement text.
###
    def replace(match: re.Match) -> str:
        nonlocal anchor_nb_HTML

        anchor_nb_HTML += 1

        return f'<a id="{TAG_ANCHOR}-{anchor_nb_HTML}"></a>\n'

    return replace


###
# prototype::
#     src   : the path of the \md file to standardise.
#     dest  : the path of the standardised final \md file to build.
#     erase : set to ''True'', this \arg allows to erase an existing
#             final file to build a new one.
#
#     :action: the ''dest'' file is a deterministic version of the
#              ''src'' file.
#
# note::
#     We use \markdown_it to transform the \md file into an \html one,
#     the latter being transformed into a \md file by \markdownify.
#     This makes it possible to manage the use of \html code in the
#     initial \src file.
###
def stdit(
    src  : Path,
    dest : Path,
    erase: bool = False
) -> None:
# Can we erase an existing file?
    if not erase and dest.is_file():
        raise IOError(
            f"the function ''stdit'' is not allowed to erase "
             "the final file:"
             "\n"
            f"{dest}"
        )

# \Html version keeping a possible ''::TOC::'' placeholder.
    mdit = MarkdownIt(
        options_update = {'html': True}
    )

    html = mdit.render(
        src.read_text(encoding = "utf8")
    )

# \Md standardized version keeping a possible ''::TOC::''.
    sdtconv = StdConverter(bullets = '-'*3)
    md_std  = sdtconv.convert(html)
    md_std += "\n"

# Management of ''::TOC::''.
    nb_tag_TOC = sdtconv.nb_tag_TOC
    depth_TOC  = sdtconv.depth_TOC
    all_titles = sdtconv.titles

# Misuse of ''::TOC::''.
    if nb_tag_TOC > 1:
        raise ValueError(f"too many ''{TAG_TOC}'' used.")

# Remove unused title anchors.
    anchor_nbs_kept = []

    for (title, level, anchor_nb) in all_titles:
        if (
            nb_tag_TOC == 1
            and
            level - 1 <= depth_TOC
        ):
            anchor_nbs_kept.append(anchor_nb)

        else:
            md_std = md_std.replace(
                TAG_TMP_MD_ANCHOR.format(anchor_nb, ''),
                ''
            )

# We have to build the \toc.
    if nb_tag_TOC == 1:
# Consecutive anchor numbers is prettier.
        md_std = PATTERN_TMP_ANCHOR.sub(
            update_anchor_HTML(),
            md_std
        )

# The \toc itself.
        old_lines     = md_std.split('\n')
        md_std        = []
        anchor_nb_TOC = -1

        for line in old_lines:
# \toc placeholder found.
            if line == TAG_TMP_TOC:
                toc_html = []

                for i, (title, level, anchor_nb) in enumerate(all_titles):
                    if not anchor_nb in anchor_nbs_kept:
                        continue

                    anchor_nb_TOC += 1

                    tab   = "    "*(level - 2)
                    title = title.replace("\n", "</br>")

                    toc_html.append(
                        f"{tab}- [{title}](#{TAG_ANCHOR}-{anchor_nb_TOC})"
                    )

                line = "\n".join(toc_html)

# New line to store.
            md_std.append(line)

        md_std = "\n".join(md_std)

# Nothing left to do.
    dest.touch()
    dest.write_text(
        data     = md_std,
        encoding = "utf8"
    )
