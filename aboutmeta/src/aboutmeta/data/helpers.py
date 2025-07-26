#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #


# -------------------------- #
# -- READY-TO-USE HELPERS -- #
# -------------------------- #

HELPERS_CONTENT = {
    "project": "This block allows to describe a project from a technical point of view.",
    "project.version": "This is the current version number of the project.",
    "project.date": "This is the date of the current version of the project.",
    "project.acronym": "This information explains the meaning of the acronym used to name the project.",
    "project.codename": "This value, optional for a code-type project, allows to name the project differently from the folder containing it.",
    "project.doctitle": "This value is mandatory for a “document” type project: it gives the title of the document.",
    "project.desc": "You need to describe shortly your project.",
    "project.author": "For a single author, you have the following possible syntaxes.\n\n  + ''Krivine'' , ''Louis, Krivine'' and ''Jean, Louis, Krivine'' are legal titles for a person (the number of first names is unlimited).\n\n  + ''Krivine [jlk@brain.fr]'' adds an email.\n\n  + ''Krivine (L'Institut du Cerveau, France)'' adds an institute.\n\n  + ''Krivine [jlk@brain.fr] (L'Institut du Cerveau, France)'' mixes the previous features.",
    "project.authors": "For severals authors, just use a YAML list of single authors (see the description of the key ''author'').",
    "project.contrib": "For a single contributor, the syntaxes allowed are similar to the ones for a single author (see the key ''author'').",
    "project.contribs": "For severals authors, just use a YAML list of single authors (see the description of the key ''author'').",
    "project.urls": "Three kinds of URL can be given.\n\n  + ''home'' is for the website of the project, the human one.\n\n  + ''dev'' is dedicated to the repository of the project, this is not intended for human beings.\n\n  + ''issues'' allows regular users to report bugs.",
    "project.licenses": "Granting a license is a good practice.\n\n  + ''code'' is for the code of the project.\n\n  + ''manual'' is for the manual of the project.",
    "project.langs": "This for the language used to write the manual (manual) and the technical (doc) documentations.",
    "project.require": "Don't forget to give the list of the required general tools needed to make your project functional.",
    "project.keywords": "Providing a list of keywords describing the project helps to better understand its usefulness.",
    "toc": "Using hard-coded paths, or glob or regex patterns, you select a list of absolute paths of existing files. Here are the available features, with paths searched inside the folder of the ''about.yaml'' file.\n\n  + ''/hard/coded/path/one/file'' indicates a specific file.\n\n  + ''/hard/coded/path/about/subfolder'' indicates a specific folder containing a new ''about.yaml'' file to be analyzed.\n\n  + ''glob: ...'' allows to use the glob syntax, and for a recursive search, there is ''r-glob: ...''.\n\n  + ''regex: ...'' allows to use regex patterns, and ''r-regex: ...''     is available for recursive searches.",
}
