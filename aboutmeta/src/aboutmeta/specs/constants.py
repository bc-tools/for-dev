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


# --------------- #
# -- META TAGS -- #
# --------------- #

TAG_SPECS_ALT_ALL = "__ALT_ALL__"
TAG_SPECS_ALT_TUPLES = "__ALT_TUPLES__"
TAG_SPECS_BLOCK = "__BLOCK__"
TAG_SPECS_CONTENT = "__CONTENT__"
TAG_SPECS_DATA = "__DATA__"
TAG_SPECS_LIST_OF = "__LIST_OF__"
TAG_SPECS_POST_PROD = "__POST-PROD__"
TAG_SPECS_PARSER = "__PARSER__"
TAG_SPECS_REQUIRED = "__REQUIRED__"
TAG_SPECS_OPTIONAL = "__OPTIONAL__"
TAG_SPECS_TYPE = "__TYPE__"

TAG_ARG_AMDATA_CLS = "amdata_cls"
TAG_ARG_DATA = "data"
TAG_ARG_DATA_LIST = "data_list"
TAG_ARG_PARENT = "parent"
