#!/usr/bin/env python3

from rich import print

from utilities.cnp_code import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

MAGIC_COMMENT_HELPER = "#"*3

PATTERN_KEEP_BEFORE_SPACES = re.compile(r'^(\s*)(.*)')
PATTERN_MULTI_SPACES       = re.compile(r'\s{2,}')
PATTERN_SECTION_TITLE      = re.compile(r'^\{(.*)\}$')


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

def build_helpers(
    context,
    this_dir,
    contrib_dir_name,
    nbtest,
    subfolder,
):
    (
        projdir,
        projname,
        contribdir,
        statusdir,
        srcdir,
        testsdir
    ) = get_specs_folders(
        context          = context,
        this_dir         = this_dir,
        contrib_dir_name = contrib_dir_name,
        nbtest           = nbtest,
        subfolder        = subfolder,
    )

    allfiles = get_accepted_paths(
        context    = context,
        contribdir = contribdir,
        statusdir  = statusdir,
        subfolder  = context,
        ext        = 'yaml',
    )

# Nothing added...
    if not allfiles:
        logging.warning("No file found!")

# We have to work.
    else:
        exit()


        for yfile in allfiles:
            helpers = extract_helpers(yfile)

            print(helpers)




def extract_helpers(yaml_file):
    src_code = yaml_file.read_text()

    helpers        = dict()
    is_helper_doc  = False
    pre_helper_doc = []


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

                pre_helper_doc.append(line)

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

            if pre_helper_doc:
                str_paths          = '.'.join(cur_paths)
                helpers[str_paths] = pre_helper_doc
                pre_helper_doc         = []

# Nothing left to do.
    return helpers








def update_helpers(
    cur_paths : list[str],
    pre_helper_doc: list[str]
) -> None:
    global HELPERS

# Helper content.
    helper_content = unwrapped_content(pre_helper_doc)

# What is documented?
    cur_paths = build_pointed_paths(cur_paths)
    last_keys = get_last_keys(cur_paths)

# Just one thing, nothing left to do.
    if len(last_keys) == 1:
# Several paths can go to the same last key!
        for p in cur_paths:
            HELPERS[p] = helper_content

# Severals docs for different keys.
    else:
        HELPERS |= extract_sub_section(cur_paths, pre_helper_doc)



def unwrapped_content(lines: list[str]) -> str:
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
    paths: list[str],
    lines: list[str]
) -> dict[str, str]:
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


def build_pointed_paths(pointed_path: str) -> list[str]:
    parts =  [
        split_path_part(p)
        for p in pointed_path
    ]

    return _recu_all_paths(parts)


def split_path_part(path_part: str) -> list[str]:
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


def _recu_all_paths(parts: list[str]) -> list[str]:
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


def get_last_keys(paths: list[str]) -> set[str]:
    return set(
        p.split('.')[-1]
        for p in paths
    )
