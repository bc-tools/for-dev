#!/usr/bin/env python3

###
# This module allows to make a single \md file from several single ones
# (using or not an "automatic" merging).
###


from pathlib import Path

from .about     import *
from .normalize import *


# --------------------------------------------- #
# -- SINGLE \MD FROM \MD NOMRLAIZED CHUNKS -- #
# --------------------------------------------- #

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
# This class finds all the single \md files and then builds a final
# single one with all the chunks found.
###
class Builder:
    mdit = MarkdownIt(
        options_update = {'html': True}
    )

###
# prototype::
#     src   : the path of the \dir containing the \md chunks.
#     dest  : the path of the single final \md file to build.
#     erase : set to ''True'', this \arg allows to erase an existing
#             final file to build a new one.
###
    def __init__(
        self,
        src  : Path,
        dest : Path,
        erase: bool = False
    ) -> None:
        self.src   = src
        self.dest  = dest
        self.erase = erase

###
# prototype::
#     :action: this method finds the single \md files, and then merges
#              all the \md codes found to build the final \md file.
#
# note::
#     We use \markdown_it to transform the \md file into an \html one,
#     the latter being transformed into a \md file by \markdownify.
#     This makes it possible to manage the use of \html code in the
#     initial \src file.
###
    def build(self) -> None:

        self.sdtconv = StdConverter(bullets = '-'*3)

# Can we erase an existing final file?
        if self.dest.is_file() and not self.erase:
            raise IOError(
                f"the class {type(self).__name__} is not allowed "
                "to erase the final file:"
                "\n"
                f"{self.dest}"
            )

# \Html version keeping a possible ''::TOC::'' placeholder.
        self.html_code = []

        for onefile in TOC(self.src).extract():
            self.html_code.append(
                self.mdit.render(
                    onefile.read_text(encoding = "utf-8").strip()
                )
            )

        self.html_code = "\n".join(self.html_code)

# \Md standardized version keeping a possible ''::TOC::''.
        self.std_md_code  = self.sdtconv.convert(self.html_code)

# Management of ''::TOC::''.
        self.tocify()

        self.std_md_code += "\n"


# Final \md standardized single version.
        self.dest.touch()

        self.dest.write_text(
            data     = self.std_md_code,
            encoding = "utf-8"
        )

###
# prototype::
#     :action: ????
###
    def tocify(self) -> None:
        md_std = self.std_md_code

        nb_tag_TOC = self.sdtconv.nb_tag_TOC
        depth_TOC  = self.sdtconv.depth_TOC
        all_titles = self.sdtconv.titles

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

# Let's publish our workd...
        self.std_md_code = md_std
