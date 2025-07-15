#### Working with folders and files

The list of paths is validated during digestion and is returned as a list of pairs `pathlib.Path` objects that complies with the following specifications.

  1. The boolean value is `True` for a path pointing to a file, and `False` for a folder.

  1. The path is a `pathlib.Path` object.


> ***NOTE.*** *Paths must point to existing folders and files.*
