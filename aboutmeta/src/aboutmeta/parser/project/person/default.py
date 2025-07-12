# ------------- #
# -- IMPORTS -- #
# ------------- #

from ....data import constants
from ....data import person
from ....tool import group


# -------------------- #
# -- IMPLEMENTATION -- #
# -------------------- #

###
# prototype::
#     content : one person provided in the \yaml file, but stripped.
#
#     :return: an instance of the class ''aboutmeta.data.person.Person''
#              to work easily with the person data.
###
def parser(content: str) -> person.Person: # abc  #def
# One affiliation?
    content, affiliation = group.extract_group(#
        content = content,
        opener  = constants.TAG_AFFILIATION_OPEN,#
        closer  = constants.TAG_AFFILIATION_CLOSE,#
        context = "affiliation"
    )

# One email?
    content, email = group.extract_group(#
        content = content,
        opener  = constants.TAG_EMAIL_OPEN,#
        closer  = constants.TAG_EMAIL_CLOSE,#
        context = "email"
    )

# Titles of the person.
    titles = content.split(',')

    if len(titles) == 1:
        firstnames = None

    else:
        firstnames = [
            n.strip() for n in titles[:-1]
        ]

    surname = titles[-1].lstrip()

# The job has been done.
    return person.Person(#
        firstnames  = firstnames,
        surname     = surname,
        email       = email,
        affiliation = affiliation
    )