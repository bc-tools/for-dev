




# ------------------ #
# -- SOURCE CODES -- #
# ------------------ #






# --------------------------- #
# -- FILES FOR UNIT TESTS? -- #
# --------------------------- #

print(f"{ITEM_1} Verifying the existence of test files...")

# Test files implemented.
test_files  = defaultdict(set)
no_pb_found = True

for test_file in TESTS_DIR.glob("**/test_*.py"):
    test_file = test_file.relative_to(TESTS_DIR)

    data_type = str(test_file.parents[0])
    syntax    = test_file.stem

    match = PATTERN_TEST_NAME.search(syntax)

    if match:
        test_files[data_type].add(match.group("syntax"))

# Tests needed.
for data_type, syntaxes in contrib_files.items():
    if not data_type in test_files:
        no_pb_found = False

        print(f"{ITEM_2} Zero test files for ''{data_type}'' parsers.")

    elif test_files[data_type] != contrib_files[data_type]:
        no_pb_found = False

        unexpected = test_files[data_type] - contrib_files[data_type]
        missing    = contrib_files[data_type] - test_files[data_type]

        if missing:
            print(f"{ITEM_2} Missing test files for ''{data_type}'' parsers.")

            missing = list(missing)
            missing.sort()
            missing = f"\n{ITEM_3}".join(missing)

            print(f"{ITEM_3} {missing}")

        if unexpected:
            print(f"{ITEM_2} Unexpected test files for ''{data_type}'' parsers.")

            unexpected = list(unexpected)
            unexpected.sort()
            unexpected = f"\n{ITEM_3}".join(unexpected)

            print(f"{ITEM_3} {unexpected}")

# Conclusion.
if no_pb_found:
    print(f"{ITEM_2} No test files missing.")
