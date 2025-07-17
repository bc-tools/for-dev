#### Working with folders and files

The list of reltive paths is validated during parsing and is returned as a list of `pathlib.Path` objects pointing to files (the absolute path is used). The order of the list follows the logic of using multiple `toc` blocks when using folder paths.
