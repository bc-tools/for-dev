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

# Human tests?
        if not SECTION_TESTS in hd_split_pyfile(contrib_file):
            log_raise_error(
                context = "contrib",
                desc    = (
                    f"No unit tests validated: "
                    f"'{contrib_file}'."
                ),
                exception = ValueError,
            )

# Look at the code.
        final_code = finalize_pycode(
            file        = contrib_file,
            hds_ignored = HEADERS_IGNORED
        )

        if not final_code:
            log_raise_error(
                context = "contrib",
                desc    = (
                    f"Empty file validated: "
                    f"'{contrib_file}'."
                ),
                exception = ValueError,
            )

# Good signatures?
        if ctxt == CTXT_PARSER:
            validate_signatures(
                ctxt        = f"Contrib. {ctxt}",
                desc        = "Illegal contrib validation",
                legal_signs = LEGAL_SIGNS,
                file        = contrib_file,
                code        = final_code,
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
