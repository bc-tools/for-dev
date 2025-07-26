#!/usr/bin/env python3

from typing import List, Set, Dict

from pathlib import Path
import              re
from yaml    import safe_load

from black import (
    format_file_in_place,
    FileMode,
    WriteBack
)


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent

PROJECT_DIR  = THIS_DIR.parent
PROJECT_NAME = PROJECT_DIR.name

SPECS_DIR = PROJECT_DIR / "specs"

SRC_DIR         = PROJECT_DIR / "src" / PROJECT_NAME
HELPERS_FILE    = SRC_DIR / "helpers.py"
FORMATTERS_FILE = SRC_DIR / "formatters.py"

HELP_CONTENT     = {}
FORMATTING_SPECS = {}

MAGIC_COMMENT_HELPER = "#"*3


PATTERN_KEEP_BEFORE_SPACES = re.compile(r'^(\s*)(.*)')
PATTERN_MULTI_SPACES       = re.compile(r'\s{2,}')


# ----------- #
# -- TOOLS -- #
# ----------- #

def extract_helpers(yaml_file):
    src_code = yaml_file.read_text()

    is_helper_doc = False
    helper_doc    = []

    last_level = 100 # Bigger than any real level!
    cur_paths  = []

    for nb, line in enumerate(src_code.split("\n"), start = 1):
        if not line:
            continue

# Helping magic comment start or end?
        if line == MAGIC_COMMENT_HELPER:
            is_helper_doc = not is_helper_doc

# Comment...
        elif line[0] == '#':
# ... giving one line in the helper.
            if is_helper_doc:
                line = line[1:]

                if line:
                    line = line[1:]

                helper_doc.append(line)

# YAML specs.
        else:
            if is_helper_doc:
                raise ValueError(
                    f"misuse of magic comments at line {nb}. "
                    f"See the file:\n{yaml_file}"
                )

            level = (len(line) - len(line.lstrip())) // 2

            if level <= last_level:
                for _ in range(last_level - level + 1):
                    if not cur_paths:
                        break

                    cur_paths.pop(-1)

            last_level =level

            cur_paths.append(line)

            if helper_doc:
                update_helpers(
                    cur_paths,
                    helper_doc
                )

                helper_doc = []


def update_helpers(
    cur_paths : List[str],
    helper_doc: List[str]
) -> None:
    global HELP_CONTENT

# Helper content.
    helper_content = []
    block_content  = []

    for line in helper_doc:
        if line:
            block_content.append(line)

        else:
            block_content = ' '.join(block_content)

            match = PATTERN_KEEP_BEFORE_SPACES.match(block_content)

            prespaces = match.group(1)
            content   = match.group(2)

            content = PATTERN_MULTI_SPACES.sub(' ', content)

            helper_content.append(prespaces + content)
            helper_content.append('')

            block_content  = []

    if block_content:
        helper_content.append(' '.join(block_content))

    helper_content = '\n'.join(helper_content)

# What is documented?
    cur_paths = build_pointed_paths(cur_paths)
    last_keys = set(
        p.split('.')[-1]
        for p in cur_paths
    )

# Just one thing, nothing left to do.
    if len(last_keys) == 1:
        helper_doc = "\n".join(helper_doc)

        for p in cur_paths:
            HELP_CONTENT[p] = helper_doc

# Severals docs at the same time.
    else:
        print(f"{cur_paths=}")
        print(extract_sub_section(last_keys, helper_doc))
        exit()
    # cur_paths = ".".join(cur_paths)

# Do we have the expecetd sections?

# Everything looks good.


def extract_sub_section(
    keys_expected: Set[str],
    lines        : List[str]
) -> Dict[str, str]:
    print(keys_expected)
    print(lines)
    exit()

def build_pointed_paths(pointed_path: str) -> List[str]:
    parts =  [
        split_path_part(p)
        for p in pointed_path
    ]

    return _recu_all_paths(parts)


def _recu_all_paths(parts: List[str]) -> List[str]:
    if not parts:
        return parts

    final_parts = []

    for p in parts[0]:
        sub_parts = _recu_all_paths(parts[1:])

        if sub_parts:
            for sp in sub_parts:
                final_parts.append(f"{p}.{sp}")

        else:
            final_parts.append(p)

    return final_parts


def split_path_part(path_part: str) -> List[str]:
    path_part = path_part.split(':')[0]
    path_part = path_part.strip()

    if path_part[-1] == "*":
        path_part = path_part[:-1]
        path_part = path_part.strip()

    path_part = [
        sp.strip()
        for sp in path_part.split('|')
    ]

    return path_part

# ------------------------------------- #
# -- ANALYZING SOURCES OF YAML SPECS -- #
# ------------------------------------- #

for yaml_file in SPECS_DIR.glob("*.yaml"):
    extract_helpers(yaml_file)

from pprint import pprint;pprint(HELP_CONTENT)
