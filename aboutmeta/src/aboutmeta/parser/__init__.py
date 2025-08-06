#!/usr/bin/env python3

from .date import parse as date_parse
from .lang import parse as lang_parse
from .license import parse as license_parse
from .person import parse as person_parse
from .sem_version import parse as sem_version_parse
from .url import parse as url_parse
from .virtual_path import parse as virtual_path_parse

ALL_PARSERS = {
    "date": date_parse,
    "lang": lang_parse,
    "license": license_parse,
    "person": person_parse,
    "sem_version": sem_version_parse,
    "url": url_parse,
    "virtual_path": virtual_path_parse,
}
