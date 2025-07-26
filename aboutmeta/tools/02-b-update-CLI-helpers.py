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

SRC_DIR      = PROJECT_DIR / "src" / PROJECT_NAME
HELPERS_FILE = SRC_DIR / "data" / "helpers.py"

HELPERS_CONTENT = {}

MAGIC_COMMENT_HELPER = "#"*3


PATTERN_KEEP_BEFORE_SPACES = re.compile(r'^(\s*)(.*)')
PATTERN_MULTI_SPACES       = re.compile(r'\s{2,}')
PATTERN_SECTION_TITLE      = re.compile(r'^\{(.*)\}$')


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

            last_level = level

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
    global HELPERS_CONTENT

# Helper content.
    helper_content = unwrapped_content(helper_doc)

# What is documented?
    cur_paths = build_pointed_paths(cur_paths)
    last_keys = get_last_keys(cur_paths)

# Just one thing, nothing left to do.
    if len(last_keys) == 1:
# Several paths can go to the same last key!
        for p in cur_paths:
            HELPERS_CONTENT[p] = helper_content

# Severals docs for different keys.
    else:
        HELPERS_CONTENT |= extract_sub_section(cur_paths, helper_doc)


def unwrapped_content(lines: List[str]) -> str:
    content = []
    block   = []

    for l in lines:
        if l:
            block.append(l)

        else:
            block = ' '.join(block)

            match = PATTERN_KEEP_BEFORE_SPACES.match(block)

            prespaces  = match.group(1)
            postspaces = match.group(2)

            postspaces = PATTERN_MULTI_SPACES.sub(' ', postspaces)

            content.append(prespaces + postspaces)
            content.append('')

            block = []

    if block:
        content.append(' '.join(block))

    content = '\n'.join(content)

    return content.strip()


def extract_sub_section(
    paths: List[str],
    lines: List[str]
) -> Dict[str, str]:
# Looking for sections.
    inter_sections = {}

    last_title   = ''
    last_content = []

    for l in lines:
        match = PATTERN_SECTION_TITLE.match(l)

        if match is None:
            last_content.append(l)
            continue

        if last_title in inter_sections:
            TODO

        if last_content:
            inter_sections[last_title] = gather_content(last_title, last_content)

        last_title   = match.group(1)
        last_content = []

    inter_sections[last_title] = gather_content(last_title, last_content)

# No extra or unknown sections?
    titles    = set(inter_sections)
    last_keys = get_last_keys(paths)

    if titles != last_keys:
        TODO

# Final sections?
    sections = {}

    for p in paths:
        title = p.split('.')[-1]

        sections[p] = inter_sections[title]

    return sections


def gather_content(
    title          : str,
    section_content: List[str]
) -> str:
    section_content = unwrapped_content(section_content)

    if not section_content:
        TODO

    return section_content


def build_pointed_paths(pointed_path: str) -> List[str]:
    parts =  [
        split_path_part(p)
        for p in pointed_path
    ]

    return _recu_all_paths(parts)


def get_last_keys(paths: List[str]) -> Set[str]:
    return set(
        p.split('.')[-1]
        for p in paths
    )


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

# Nothing left to do.
HELPERS_FILE.touch()
HELPERS_FILE.write_text(
    f"""
#!/usr/bin/env python3

# ------------------------------------------------------- #
# -- File created automatically from YAML spec. files. -- #
# --                                                   -- #
# -- Formatting done by the Python project "black".    -- #
# ------------------------------------------------------- #


# -------------------------- #
# -- READY-TO-USE HELPERS -- #
# -------------------------- #

HELPERS_CONTENT = {HELPERS_CONTENT}
    """.strip() + '\n'
)

format_file_in_place(
    HELPERS_FILE,
    fast       = False,
    mode       = FileMode(),
    write_back = WriteBack.YES,
)
