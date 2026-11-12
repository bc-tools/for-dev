### A few block structure tests

To validate the block contract, you need to provide both valid and invalid sample `YAML` files that test block structures, but not flavors. The focus is on verifying the overall structure rather than testing every individual value. For instance, include a file with a minimal structure, one with a maximal structure, and examples that violate specific rules (such as conflicting keys or missing required keys). These test files are located in the `block-syntax/tests/ok` and `block-syntax/tests/ko` directories.


> ***IMPORTANT.*** *You can use `...` as a placeholder for values. They are not checked at this level: data and parsers are tested separately, and combined structure/value errors are covered automatically.*


> ***CAUTION.*** *For all valid key paths, the contents are not parsed. For example, if the `version` key expects a number-like data, the validation tests will not flag a potential use of `version: invalid: 4`."*
