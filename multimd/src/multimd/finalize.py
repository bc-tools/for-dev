###
# This module ????    allows to make a single path::''MD'' file from several single
# ones (using or not an "automatic" merging).
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

TAG_TOC     = "::TOC::"
TAG_TMP_TOC = "::M+u-L+t-I+m-D=T-o+C::"
PATTERN_TOC = re.compile(rf"::TOC(-(\d+))?::")

TAG_ANCHOR         = "MULTIMD-TOC-ANCHOR"
TAG_TMP_MD_ANCHOR  = f"::{TAG_ANCHOR}-{{}}::\n{{}}"
PATTERN_TMP_ANCHOR = re.compile(rf"::{TAG_ANCHOR}-\d+::\n")



# ------------------------------------ #
# -- XXXX -- #
# ------------------------------------ #

###
# XXXX
###
class StdConverter(MarkdownConverter):
###
# XXXX
###
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.anchor_nb  = -1
        self.nb_tag_TOC = 0
        self.depth_TOC  = 100 # "Infinite" depth....
        self.titles     = []

    def process_text(self, el, parent_tags = None):
        text = super().process_text(el, parent_tags)

# Do we have a placeholder for a ToC?
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
# XXXX
###
    def _convert_hn(self, n, el, text, parent_tags = None):
        title = super()._convert_hn(n, el, text, parent_tags)

        print((parent_tags, n))
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
# XXXX
###
    def convert_code(self, el, text, parent_tags = None):
        # Ne pas traiter si on est dans un bloc <pre>
        if el.parent.name == "pre":
            return text

        code = el.get_text()

        if "`" in code:
            code = f"`{code}`"

        return f"`{code}`"

###
# XXXX
###
    def convert_pre(self, el, text, parent_tags = None):
        code_el = el.find("code")

        if code_el:
            lang_classes = code_el.get("class", [])
            lang = ""

            for cls in lang_classes:
                if cls.startswith("language-"):
                    lang = cls.replace("language-", "")
                    break

            code = code_el.get_text()

        else:
            lang = ""
            code = el.get_text()

        return f"\n~~~{lang}\n{code.strip()}\n~~~\n"

###
# XXXX
###
def _update_anchor_HTML():
    anchor_nb_HTML = -1

    def replace(match):
        nonlocal anchor_nb_HTML

        anchor_nb_HTML += 1

        return f'<a id="MULTIMD-TOC-ANCHOR-{anchor_nb_HTML}"></a>\n'

    return replace

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

# MD nomralized version keeping possible ''::TOC::''.
    mdit = MarkdownIt(
        options_update = {
            # 'breaks': True,
            'html'  : True
        }
    )

    md_std = mdit.render(
        src.read_text(encoding = "utf8")
    )

    sdtconv = StdConverter(bullets = '-'*3)
    md_std  = sdtconv.convert(md_std)
    md_std += "\n"

# Management of ''::TOC::''.
    nb_tag_TOC = sdtconv.nb_tag_TOC
    depth_TOC  = sdtconv.depth_TOC
    all_titles = sdtconv.titles

# Misuse of ''::TOC::''.
    if nb_tag_TOC > 1:
        raise ValueError(
            f"Too many ''{TAG_TOC}'' used."
        )

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
            md_std = md_std.replace(TAG_TMP_MD_ANCHOR.format(anchor_nb, ''), '')


# We have to build the ToC.
    if nb_tag_TOC == 1:
# Consecutive anchor numbers is prettier.
        md_std = PATTERN_TMP_ANCHOR.sub(_update_anchor_HTML(), md_std)

# The ToC itself.
        old_lines     = md_std.split('\n')
        md_std        = []
        anchor_nb_TOC = -1

        for line in old_lines:
            if line == TAG_TMP_TOC:
                toc_html = []

                for i, (title, level, anchor_nb) in enumerate(all_titles):
                    if not anchor_nb in anchor_nbs_kept:
                        continue

                    anchor_nb_TOC += 1

                    tab   = "  "*(level - 2)
                    title = title.replace("\n", "</br>")

                    toc_html.append(
                        f"{tab}- [{title}](#{TAG_ANCHOR}-{anchor_nb_TOC})"
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
