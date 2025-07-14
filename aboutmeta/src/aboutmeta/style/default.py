#!/usr/bin/env python3

from dataclasses import dataclass

import aboutmeta.parser.date.default as date_default
import aboutmeta.parser.lang.default as lang_default
import aboutmeta.parser.license.default as license_default
import aboutmeta.parser.person.default as person_default
import aboutmeta.parser.version.default as version_default


# --------------------- #
# -- DEFAULT PARSERS -- #
# --------------------- #

@dataclass
class Parsers:
    date = date_default.parser
    lang = lang_default.parser
    license = license_default.parser
    person = person_default.parser
    version = version_default.parser
