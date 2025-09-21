#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #

from aboutmeta.specs.parser.date import parse as date_parse
from aboutmeta.specs.parser.lang import parse as lang_parse
from aboutmeta.specs.parser.license import parse as license_parse
from aboutmeta.specs.parser.person import parse as person_parse
from aboutmeta.specs.parser.sem_version import parse as sem_version_parse
from aboutmeta.specs.parser.url import parse as url_parse
from aboutmeta.specs.parser.virtual_path import parse as virtual_path_parse
from aboutmeta.specs.mapper.virtual_path import map_list as virtual_path_map


# ---------- #
# -- TAGS -- #
# ---------- #

TAG_SPECS_ALT_ALL = "__ALT_ALL__"
TAG_SPECS_ALT_TUPLES = "__ALT_TUPLES__"
TAG_SPECS_BLOCK = "__BLOCK__"
TAG_SPECS_CONTENT = "__CONTENT__"
TAG_SPECS_DATA = "__DATA__"
TAG_SPECS_LIST_OF = "__LIST_OF__"
TAG_SPECS_MAPPER = "__MAPPER__"
TAG_SPECS_PARSER = "__PARSER__"
TAG_SPECS_REQUIRED = "__REQUIRED__"
TAG_SPECS_OPTIONAL = "__OPTIONAL__"
TAG_SPECS_TOOLS = "__TOOLS__"
TAG_SPECS_TYPE = "__TYPE__"

TAG_ARG_AMDATA_CLS = "amdata_cls"
TAG_ARG_DATA = "data"
TAG_ARG_DATA_LIST = "data_list"
TAG_ARG_PARENT = "parent"

TAG_KEY_ACRONYM = "acronym"
TAG_KEY_AUTHOR = "author"
TAG_KEY_AUTHORS = "authors"
TAG_KEY_CODE = "code"
TAG_KEY_CODENAME = "codename"
TAG_KEY_CONTRIB = "contrib"
TAG_KEY_CONTRIBS = "contribs"
TAG_KEY_DATE = "date"
TAG_KEY_DESC = "desc"
TAG_KEY_DEV = "dev"
TAG_KEY_DOC = "doc"
TAG_KEY_DOCTITLE = "doctitle"
TAG_KEY_HOME = "home"
TAG_KEY_ISSUES = "issues"
TAG_KEY_KEYWORDS = "keywords"
TAG_KEY_LANGS = "langs"
TAG_KEY_LICENSES = "licenses"
TAG_KEY_MANUAL = "manual"
TAG_KEY_PROJECT = "project"
TAG_KEY_REQUIRE = "require"
TAG_KEY_TOC = "toc"
TAG_KEY_URLS = "urls"
TAG_KEY_VERSION = "version"

TAG_FLAVOUR_IT_PROJECT = "it-project"
TAG_FLAVOUR_TOC = "toc"
