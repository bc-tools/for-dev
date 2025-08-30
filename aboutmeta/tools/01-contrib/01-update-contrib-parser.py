#!/usr/bin/env python3

from pathlib import Path
import              sys

sys.path.append(str(Path(__file__).parent.parent))

from cbutils.core import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR    = Path(__file__).parent
PROJECT_DIR = THIS_DIR.parent.parent
SRC_DIR     = PROJECT_DIR / "src" / "aboutmeta" / "specs"
CONTRIB_DIR = PROJECT_DIR / "contrib"


CTXT_DATA   = 'data'
CTXT_PARSER = 'parser'

PYCODE_CONTRIB_DIRS = [
    CONTRIB_DIR / CTXT_DATA,
    CONTRIB_DIR / CTXT_PARSER,
]
PYCODE_CONTRIB_DIRS = [p / "code" for p in PYCODE_CONTRIB_DIRS]


HEADERS_IGNORED = [
    (SECTION_TESTS:= "TESTS"),
    (SECTION_TOOLS:= "TOOLS"),
]


SIGNATURES = {
    'parse'   : (
# is_mandatory, authorised_signs
        True,
        [
            set(['data']),
            set(['amdata_cls', 'data'])
        ]
    ),
    'map_list': (
        False,
        [
            set(['data_list']),
            set(['amdata_cls', 'data_list'])
        ]
    ),
}


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# prototype::
#     file : XXX
#
#     :return: XXX
###
def get_xtra_files(file: Path) -> list[Path]:
    xtra_files = [
        p
        for p in file.parent.glob(
            f"{file.stem}-*"
        )
        if p != file
    ]

    return xtra_files

###
# prototype::
#     ctxt : XXX
#     code : XXX
#
#     :action: XXX
###
def validate_signatures(
    ctxt: str,
    code: str,
) -> None:
    if ctxt == CTXT_PARSER:
        for func_name, (
            is_mandatory,
            authorised_signs
        ) in SIGNATURES.items():
            sign = get_parse_signature(
                code         = code,
                func_name    = func_name,
                is_mandatory = is_mandatory,
            )

            if sign is None:
                continue

            if not sign in authorised_signs:
                if len(authorised_signs) == 1:
                    helper = ["One authorised signature."]

                else:
                    helper = ["Authorised signatures."]

                helper += [
                    f"  + {func_name}({', '.join(sorted(s))})" for s in authorised_signs
                ]

                helper = '\n'.join(helper)

                sign = f"({', '.join(sorted(sign))})"

                log_raise_error(
                    context = f"Contrib. {ctxt}",
                    desc    = (
                            "Illegal contrib. validation: "
                        f"unauthorised signature '{sign}' for "
                        f"'{func_name}' function in file: "
                        f"'{contrib_file}'"
                    ),
                    exception = ValueError,
                    xtra      = f"\n\n{helper}",
                )


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

add_missing_init(SRC_DIR)

for folder, contribs in get_accepted_paths(PROJECT_DIR).items():
    if not folder in PYCODE_CONTRIB_DIRS:
        continue

    ctxt = folder.parent.name

    logging.info(f"Working on '{ctxt}'.")

    dest_dir = SRC_DIR / ctxt

    add_missing_dir(dest_dir)
    add_missing_init(dest_dir)

    for one_contrib in contribs:
# New Python code.
        contrib_file = folder / one_contrib

        final_code = finalize_pycode(
            file            = contrib_file,
            headers_ignored = HEADERS_IGNORED
        )

        if not final_code:
            log_raise_error(
                exception = ValueError,
                context   = "contrib",
                desc      = (
                    f"Empty file validated: "
                    f"'{contrib_file.relative_to(PROJECT_DIR)}'."),
            )

# Good signatures?
        validate_signatures(
            ctxt = ctxt,
            code = final_code,
        )

# We can create / update the source file.
        create_update_file(
            file    = dest_dir / one_contrib,
            content = final_code,
        )

# Extra files to add?
        xtra_files = get_xtra_files(contrib_file)

        if xtra_files:
            plurial = "" if len(xtra_files) == 1 else "s"

            logging.warning(f"Extra file{plurial} used.")

            for xfile in xtra_files:
                create_update_file(
                    file      = dest_dir / xfile.name,
                    content   = xfile.read_text() + "\n",
                    log_level = TAG_WARNING
                )
