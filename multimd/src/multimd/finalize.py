from pathlib import Path

# No need to rebuild a wheel...
from markdown_it import MarkdownIt
from markdownify import (
    MarkdownConverter,
    markdownify,
)


TAG_TOC           = "::TOC::"
TAG_ANCHOR        = "MULTIMD-TOC-ANCHOR"
TAG_TMP_MD_ANCHOR = f"::{TAG_ANCHOR}-{{}}::\n{{}}"

###
# XXXX
###
class StdConverter(MarkdownConverter):
###
# XXXX
###
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.anchor_nb = 0

###
# XXXX
###
    def convert_hN(self, n, el, text, parent_tags):
        title = super().convert_hN(n, el, "text", parent_tags)

        n = max(1, min(6, n))

        if n > 1:
            self.anchor_nb += 1

            title = TAG_TMP_MD_ANCHOR.format(
                self.anchor_nb,
                title
            )

        return title

###
# XXXX
###
    def convert_code(self, el, text, parent_tags):
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
    def convert_pre(self, el, text, parent_tags):
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
    print(sdtconv.anchor_nb)

# Nothing left to do.
    dest.touch()
    dest.write_text(
        data     = md_std,
        encoding = "utf8"
    )
